from itertools import groupby

import numpy as np
import torch
from transformers import squad_convert_examples_to_features, is_tf_available
from transformers.pipelines import QuestionAnsweringPipeline, SUPPORTED_TASKS

if is_tf_available():
    import tensorflow as tf


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class OurQuestionAnsweringPipeline(QuestionAnsweringPipeline):
    def __call__(self, *texts, **kwargs):
        """
        Args:
            We support multiple use-cases, the following are exclusive:
            X: sequence of SquadExample
            data: sequence of SquadExample
            question: (str, List[str]), batch of question(s) to map along with context
            context: (str, List[str]), batch of context(s) associated with the provided question keyword argument
        Returns:
            dict: {'answer': str, 'score": float, 'start": int, "end": int}
            answer: the textual answer in the intial context
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
        features_list_all = squad_convert_examples_to_features(
            examples,
            self.tokenizer,
            kwargs["max_seq_len"],
            kwargs["doc_stride"],
            kwargs["max_question_len"],
            False,
            threads=kwargs["threads"],
        )
        features_list = [list(x) for _, x in groupby(features_list_all, lambda f: f.example_index)]

        min_null_score = 1000000  # large and positive
        all_answers = []
        for features_list_batch, examples_batch in zip(*[chunks(x, kwargs["batch_size"]) for x in [features_list,
                                                                                                   examples]]):
            fw_args_list = [self.inputs_for_model([f.__dict__ for f in features]) for features in features_list_batch]
            starts = None
            ends = None
            # Manage tensor allocation on correct device
            with self.device_placement():
                if self.framework == "tf":
                    raise NotImplementedError("tf not supported")
                else:
                    with torch.no_grad():
                        # We obtain any value for the dictionary to compute the list length (number of features).
                        features_lens = torch.tensor([len(next(iter(fw_args.values()))) for fw_args in fw_args_list],
                                                     device=self.device, dtype=torch.int16)
                        max_feature_len = features_lens.max().item()

                        fw_args_batch = {}
                        for k, v0 in fw_args_list[0].items():
                            batch_size = len(fw_args_list)
                            seq_length = len(v0[0])
                            # zeros so attention_mask extra position has zeros.
                            fw_args_batch[k] = torch.zeros(batch_size, max_feature_len, seq_length, device=self.device,
                                                           dtype=torch.int64)
                            for i, fw_args in enumerate(fw_args_list):
                                t = torch.tensor(fw_args[k], device=self.device, dtype=torch.int64)
                                fw_args_batch[k][i, :len(t)] = t

                            fw_args_batch[k] = fw_args_batch[k].view(-1, seq_length)

                        starts, ends = self.model(**fw_args_batch)

                        starts = starts.view(batch_size, max_feature_len, -1)
                        ends = ends.view(batch_size, max_feature_len, -1)

                        starts, ends = starts.cpu().numpy(), ends.cpu().numpy()

            for start, end, features, features_len, example in zip(starts, ends, features_list_batch, features_lens,
                                                                   examples_batch):
                answers = []
                for (feature, start_, end_) in zip(features, start, end):
                    # Normalize logits and spans to retrieve the answer
                    start_ = np.exp(start_) / np.sum(np.exp(start_))
                    end_ = np.exp(end_) / np.sum(np.exp(end_))

                    # Mask padding and question
                    start_, end_ = (
                        start_ * np.abs(np.array(feature.p_mask) - 1),
                        end_ * np.abs(np.array(feature.p_mask) - 1),
                    )

                    if kwargs["version_2_with_negative"]:
                        min_null_score = min(min_null_score, (start_[0] * end_[0]).item())

                    start_[0] = end_[0] = 0

                    starts, ends, scores = self.decode(start_, end_, kwargs["topk"], kwargs["max_answer_len"])
                    char_to_word = np.array(example.char_to_word_offset)

                    # Convert the answer (tokens) back to the original text
                    answers += [
                        {
                            "score": score.item(),
                            "start": np.where(char_to_word == feature.token_to_orig_map[s])[0][0].item(),
                            "end": np.where(char_to_word == feature.token_to_orig_map[e])[0][-1].item(),
                            "answer": " ".join(
                                example.doc_tokens[feature.token_to_orig_map[s]: feature.token_to_orig_map[e] + 1]
                            ),
                        }
                        for s, e, score in zip(starts, ends, scores)
                    ]

                if kwargs["version_2_with_negative"]:
                    answers.append({"score": min_null_score, "start": 0, "end": 0, "answer": ""})

                answers = sorted(answers, key=lambda x: x["score"], reverse=True)[: kwargs["topk"]]
                all_answers += answers

        if len(all_answers) == 1:
            return all_answers[0]
        return all_answers


SUPPORTED_TASKS["question-answering"]["impl"] = OurQuestionAnsweringPipeline
