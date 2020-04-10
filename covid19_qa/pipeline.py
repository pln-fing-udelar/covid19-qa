# -*- coding: utf-8 -*-
from dataclasses import dataclass
from itertools import groupby
from typing import Iterator, Tuple

import numpy as np
import scipy.special
import torch
from transformers import Pipeline, pipeline, squad_convert_examples_to_features, SquadExample
from transformers.pipelines import QuestionAnsweringPipeline, SUPPORTED_TASKS

from covid19_qa.util import chunks

Instance = SquadExample

ANSWER_SORT_FIELD = "score"
assert ANSWER_SORT_FIELD in {"score", "score_raw"}


@dataclass
class Answer:
    instance: Instance
    text: str
    score: float
    score_raw: float
    start: int
    # We keep the null scores as a reference (even if the answer is already the null one).
    null_score: float
    null_score_raw: float

    @property
    def end(self) -> int:
        return self.start + len(self.text)

    @property
    def in_context(self) -> str:
        return f"{self.instance.context_text[:self.start]}{{{{{self.text}}}}}{self.instance.context_text[self.end:]}" \
            if self.text else ""

    @property
    def sort_key(self) -> float:
        return getattr(self, ANSWER_SORT_FIELD)

    @property
    def null_sort_key(self) -> float:
        return getattr(self, f"null_{ANSWER_SORT_FIELD}")


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

        if kwargs["topk"] < 1:
            raise ValueError("topk parameter should be >= 1 (got {})".format(kwargs["topk"]))

        if kwargs["max_answer_len"] < 1:
            raise ValueError("max_answer_len parameter should be >= 1 (got {})".format(kwargs["max_answer_len"]))

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

        for batch_idx, features_batch in enumerate(chunks(features_list_flat, kwargs["batch_size"])):
            batch_size = len(features_batch)
            kwargs_as_lists = self.inputs_for_model([f.__dict__ for f in features_batch])
            # Manage tensor allocation on correct device
            with self.device_placement():
                if self.framework == "tf":
                    raise ValueError("tf not supported")
                else:
                    with torch.no_grad():
                        kwargs_as_tensors = {k: torch.tensor(v, device=self.device, dtype=torch.int64)
                                             for k, v in kwargs_as_lists.items()}
                        starts, ends = self.model(**kwargs_as_tensors)

                        start_logits_flat[batch_idx * batch_size: (batch_idx + 1) * batch_size] = starts.cpu().numpy()
                        end_logits_flat[batch_idx * batch_size: (batch_idx + 1) * batch_size] = ends.cpu().numpy()

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
            start_probs, end_probs = start_probs * (1 - p_mask), end_probs * (1 - p_mask)

            if kwargs["version_2_with_negative"]:
                min_null_score = (start_probs[:, 0] * end_probs[:, 0]).min().item()
                min_null_score_raw = (start_logits[:, 0] + start_logits[:, 0]).min().item()
            else:
                min_null_score = 0
                min_null_score_raw = -1000000

            start_probs[:, 0] = end_probs[:, 0] = 0

            feature_indices, starts, ends, scores = self.decode(start_probs, end_probs, kwargs["topk"],
                                                                kwargs["max_answer_len"])

            # Convert the answer (tokens) back to the original text
            answers = [
                Answer(
                    instance=example,
                    text=" ".join(
                        example.doc_tokens[features[i].token_to_orig_map[s]: features[i].token_to_orig_map[e] + 1]
                    ),
                    score=score.item(),
                    score_raw=(start_logits[i, s] + end_logits[i, e]).item(),
                    start=np.where(char_to_word == features[i].token_to_orig_map[s])[0][0].item(),
                    null_score=min_null_score,
                    null_score_raw=min_null_score_raw,
                )
                for i, s, e, score in zip(feature_indices, starts, ends, scores)
            ]

            if kwargs["version_2_with_negative"]:
                answers.append(Answer(
                    instance=example,
                    text="",
                    score=min_null_score,
                    score_raw=min_null_score_raw,
                    start=0,
                    null_score=min_null_score,  # The same one, as this is the null answer itself.
                    null_score_raw=min_null_score_raw,  # The same one, as this is the null answer itself.
                ))

            for answer in sorted(answers, key=lambda a: a.sort_key, reverse=True)[: kwargs["topk"]]:
                yield answer

    def decode(self, start: np.ndarray, end: np.ndarray, topk: int,
               max_answer_len: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
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
        """
        # Ensure we have batch axis
        if start.ndim == 1:
            start = start[None]

        if end.ndim == 1:
            end = end[None]

        # Compute the score of each tuple(start, end) to be the real answer
        outer = np.matmul(np.expand_dims(start, -1), np.expand_dims(end, 1))

        # Remove candidate with end < start and end - start > max_answer_len
        candidates = np.tril(np.triu(outer), max_answer_len - 1)

        #  Inspired by Chen & al. (https://github.com/facebookresearch/DrQA)
        scores_flat = candidates.flatten()
        if topk == 1:
            idx_sort = [np.argmax(scores_flat)]
        elif len(scores_flat) < topk:
            idx_sort = np.argsort(-scores_flat)
        else:
            idx = np.argpartition(-scores_flat, topk)[0:topk]
            idx_sort = idx[np.argsort(-scores_flat[idx])]

        feature_idx, start, end = np.unravel_index(idx_sort, candidates.shape)
        return feature_idx, start, end, candidates[feature_idx, start, end]


SUPPORTED_TASKS["question-answering"]["impl"] = OurQuestionAnsweringPipeline

PATH_MODEL_FOLDER = "model"


def create_qa_pipeline(path_model_folder: str = PATH_MODEL_FOLDER, device: int = -1) -> Pipeline:
    return pipeline("question-answering", model=path_model_folder, config=path_model_folder,
                    tokenizer=path_model_folder, device=device)
