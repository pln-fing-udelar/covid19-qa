# -*- coding: utf-8 -*-
from dataclasses import dataclass
from itertools import groupby
from typing import Iterator, Literal, MutableMapping, Optional, Tuple

import numpy as np
import scipy.special
import torch
from transformers import Pipeline, pipeline, squad_convert_examples_to_features, SquadExample
from transformers.pipelines import QuestionAnsweringPipeline, SUPPORTED_TASKS

from covid19_qa.util import chunks

SORT_MODE_CHOICES = {"prob", "logit"}
DEFAULT_SORT_MODE = "prob"
TYPE_SORT_MODE = Literal["prob", "logit"]

Instance = SquadExample


@dataclass(frozen=True)
class Answer:
    instance: Instance
    text: str
    prob: float
    logit: float
    start: int
    sort_mode: TYPE_SORT_MODE = DEFAULT_SORT_MODE
    null_answer: Optional["Answer"] = None  # We keep the null answer as a reference (even if this is the one).
    in_context_window_size_half: int = 100

    def __post_init__(self):
        if not self.text:  # `self` is the null answer.
            # If the answer is null, we assign the null answer as `self` here,
            # because doing it from outside in an immutable class is impossible.
            #
            # This way of assigning is a workaround because the class is immutable,
            # and it fails to assign in the common way.
            object.__setattr__(self, "null_answer", self)

    @property
    def end(self) -> int:
        return self.start + len(self.text)

    @property
    def in_context(self) -> str:
        if self.text:
            span_start = abs(self.start - self.in_context_window_size_half)
            span_end = self.end + self.in_context_window_size_half

            prefix = self.instance.context_text[span_start:self.start]
            if span_start > 0:
                prefix = "[…]" + prefix

            suffix = self.instance.context_text[self.end:span_end]
            if span_end < len(self.instance.context_text):
                suffix += "[…]"

            return f"{prefix}**{self.text}**{suffix}"
        else:
            return ""

    @property
    def sort_score(self) -> float:
        return getattr(self, self.sort_mode)

    def one_inside_the_other_one(self, another_answer: "Answer") -> bool:
        # We suppose they both refer to the same instance.
        return (self.start <= another_answer.start and another_answer.end <= self.end) \
               or (another_answer.start <= self.start and self.end <= another_answer.end)


class OurQuestionAnsweringPipeline(QuestionAnsweringPipeline):
    def __call__(self, *texts, **kwargs) -> Iterator[Answer]:
        """
        Args:
            We support multiple use-cases, the following are exclusive:
            X: sequence of SquadExample
            data: sequence of SquadExample
            question: (str, List[str]), batch of question(s) to map along with context
            context: (str, List[str]), batch of context(s) associated with the provided question keyword argument
        Returns:
            dict: {'answer': str, 'score": float, 'start": int, "end": int}
            answer: the textual answer in the initial context
            score: the score the current answer scored for the model
            start: the character index in the original string corresponding to the beginning of the answer' span
            end: the character index in the original string corresponding to the ending of the answer' span
        """
        # Set defaults values
        kwargs.setdefault("topk", 1)
        kwargs.setdefault("doc_stride", 128)
        kwargs.setdefault("max_answer_len", 15)
        kwargs.setdefault("max_seq_len", 384)
        kwargs.setdefault("max_question_len", 64)
        kwargs.setdefault("version_2_with_negative", False)
        kwargs.setdefault("batch_size", 1)
        kwargs.setdefault("threads", 1)
        kwargs.setdefault("min_score", None)  # It has priority over "topk" and it doesn't apply to the null answer.
        kwargs.setdefault("sort_mode", DEFAULT_SORT_MODE)

        if kwargs["topk"] < 1:
            raise ValueError(f"topk parameter should be >= 1 (got {kwargs['topk']})")

        if kwargs["max_answer_len"] < 1:
            raise ValueError(f"max_answer_len parameter should be >= 1 (got {kwargs['max_answer_len']})")

        if kwargs["sort_mode"] not in SORT_MODE_CHOICES:
            raise ValueError(f"sort_mode parameter should be in {SORT_MODE_CHOICES} (got {kwargs['sort_mode']})")
        sort_with_prob = kwargs["sort_mode"] == "prob"

        # Convert inputs to features
        examples = self._args_parser(*texts, **kwargs)
        features_list_flat = squad_convert_examples_to_features(
            examples,
            self.tokenizer,
            kwargs["max_seq_len"],
            kwargs["doc_stride"],
            kwargs["max_question_len"],
            False,
            threads=kwargs["threads"],
        )

        start_logits_flat = np.empty((len(features_list_flat), kwargs["max_seq_len"]))
        end_logits_flat = np.empty_like(start_logits_flat)

        max_batch_size = kwargs["batch_size"]

        for batch_idx, features_batch in enumerate(chunks(features_list_flat, max_batch_size)):
            kwargs_as_lists = self.inputs_for_model([f.__dict__ for f in features_batch])
            # Manage tensor allocation on correct device
            with self.device_placement():
                if self.framework == "tf":
                    raise ValueError("tf not supported")
                else:
                    with torch.no_grad():
                        kwargs_as_tensors = {k: torch.tensor(v, device=self.device, dtype=torch.int64)
                                             for k, v in kwargs_as_lists.items()}
                        start_indices, end_indices = self.model(**kwargs_as_tensors)

                        batch_start_idx = batch_idx * max_batch_size
                        batch_end_idx = (batch_idx + 1) * max_batch_size
                        start_logits_flat[batch_start_idx:batch_end_idx] = start_indices.cpu().numpy()
                        end_logits_flat[batch_start_idx:batch_end_idx] = end_indices.cpu().numpy()

        # Don't convert into (batch_size, max_features_len, max_seq_length)
        # because there may be a very long doc (with a lot of features; i.e., max_features_len may be very large).

        indices_and_features_iterable = groupby(enumerate(features_list_flat), lambda t: t[1].example_index)
        for example, (_, indices_and_features) in zip(examples, indices_and_features_iterable):
            indices, features = zip(*indices_and_features)

            char_to_word = np.array(example.char_to_word_offset)

            start_logits, end_logits = start_logits_flat[indices, :], end_logits_flat[indices, :]

            # Normalize logits and spans to retrieve the answer
            start_probs = scipy.special.softmax(start_logits, axis=1)
            end_probs = scipy.special.softmax(end_logits, axis=1)

            # Mask padding and question
            p_mask = np.array([feature.p_mask for feature in features])
            p_bool_mask = p_mask == 1
            start_logits[p_bool_mask], end_logits[p_bool_mask] = -np.inf, -np.inf
            start_probs[p_bool_mask], end_probs[p_bool_mask] = 0, 0

            if kwargs["version_2_with_negative"]:
                null_answer = Answer(
                    instance=example,
                    text="",
                    prob=(start_probs[:, 0] * end_probs[:, 0]).min().item(),
                    logit=(start_logits[:, 0] + start_logits[:, 0]).min().item(),
                    start=0,
                    sort_mode=kwargs["sort_mode"],
                )
            else:
                null_answer = None

            start_probs[:, 0] = end_probs[:, 0] = 0
            start_logits[:, 0] = end_logits[:, 0] = -np.inf

            if sort_with_prob:
                start_scores, end_scores = start_probs, end_probs
            else:
                start_scores, end_scores = start_logits, end_logits

            # We increase the top-k because there can be repeated answers here
            # (e.g., they start in different tokens of the same word).
            feature_indices, start_indices, end_indices = self.decode(start_scores, end_scores, 5 * kwargs["topk"],
                                                                      kwargs["max_answer_len"], sort_with_prob)

            # Convert the answer (tokens) back to the original text
            answers = (
                Answer(
                    instance=example,
                    text=" ".join(
                        example.doc_tokens[features[f].token_to_orig_map[s]: features[f].token_to_orig_map[e] + 1]
                    ),
                    prob=(start_probs[f, s] * end_probs[f, e]).item(),
                    logit=(start_logits[f, s] + end_logits[f, e]).item(),
                    start=np.where(char_to_word == features[f].token_to_orig_map[s])[0][0].item(),
                    null_answer=null_answer,
                    sort_mode=kwargs["sort_mode"],
                )
                for f, s, e in zip(feature_indices, start_indices, end_indices)
            )

            # We leave the unique answers.
            # An answer in considered non-unique if it's inside another one.
            #
            # Note that if they have the same text and they're in the same positions then only one will be kept.
            # If they have the same text but are in different positions we leave them, and this is good
            # (i.e., it's like having more evidence).
            #
            # We use `(start, end)` to uniquely identify the answer (note they answer the same `example`).
            unique_answers_by_start_and_end: MutableMapping[Tuple[int, int], Answer] = {}
            for answer in answers:
                # We iterate with copy because we may delete items.
                for start_and_end, another_answer in list(unique_answers_by_start_and_end.items()):
                    if answer.one_inside_the_other_one(another_answer):
                        if answer.sort_score > another_answer.sort_score:
                            # TODO: we could make a new answer with the widest answer (keeping the largest score).
                            #   Or other strategies with overlapping answers.
                            del unique_answers_by_start_and_end[start_and_end]
                            unique_answers_by_start_and_end[(answer.start, answer.end)] = answer
                        break
                else:
                    unique_answers_by_start_and_end[(answer.start, answer.end)] = answer

            unique_answers = list(unique_answers_by_start_and_end.values())

            unique_answers = [answer
                              for answer in unique_answers
                              if kwargs["min_score"] is None or answer.sort_score >= kwargs["min_score"]]

            if kwargs["version_2_with_negative"]:
                unique_answers.append(null_answer)

            for answer in sorted(unique_answers, key=lambda a: a.sort_score, reverse=True)[: kwargs["topk"]]:
                yield answer

    def decode(self, start: np.ndarray, end: np.ndarray, topk: int,
               max_answer_len: int, sort_with_prob: bool = True) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Take the output of any QuestionAnswering head and will generate probabilities for each span to be
        the actual answer.
        In addition, it filters out some unwanted/impossible cases like answer len being greater than
        max_answer_len or answer end position being before the starting position.
        The method supports output the k-best answer through the topk argument.

        Args:
            start: numpy array, holding individual start probabilities for each token
            end: numpy array, holding individual end probabilities for each token
            topk: int, indicates how many possible answer span(s) to extract from the model's output
            max_answer_len: int, maximum size of the answer to extract from the model's output
            sort_with_prob: bool, if to interpret the scores as probabilities (True) or as logits
        """
        # Ensure we have batch axis
        if start.ndim == 1:
            start = start[None]

        if end.ndim == 1:
            end = end[None]

        # Compute the score of each tuple(start, end) to be the real answer
        if sort_with_prob:
            candidates = np.matmul(np.expand_dims(start, -1), np.expand_dims(end, 1))
        else:
            candidates = np.expand_dims(start, -1) + np.expand_dims(end, 1)

        # Remove candidates with end < start
        candidates[..., np.tri(*candidates.shape[-2:], k=-1, dtype=bool)] = candidates.min()  # noqa
        # Remove candidates with end - start > max_answer_len
        candidates[..., ~np.tri(*candidates.shape[-2:], k=max_answer_len - 1, dtype=bool)] = candidates.min()  # noqa

        #  Inspired by Chen & al. (https://github.com/facebookresearch/DrQA)
        scores_flat = candidates.flatten()
        if topk == 1:
            idx_sort = [np.argmax(scores_flat)]
        elif len(scores_flat) < topk:
            idx_sort = np.argsort(-scores_flat)
        else:
            idx = np.argpartition(-scores_flat, topk)[0:topk]
            idx_sort = idx[np.argsort(-scores_flat[idx])]

        return np.unravel_index(idx_sort, candidates.shape)


SUPPORTED_TASKS["question-answering"]["impl"] = OurQuestionAnsweringPipeline

PATH_MODEL_FOLDER = "model"


def create_qa_pipeline(path_model_folder: str = PATH_MODEL_FOLDER, device: int = -1) -> Pipeline:
    return pipeline("question-answering", model=path_model_folder, config=path_model_folder,
                    tokenizer=path_model_folder, device=device)
