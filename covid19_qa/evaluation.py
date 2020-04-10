from numbers import Number
from typing import Iterator, Mapping, Optional

from transformers import Pipeline
from transformers.data.metrics.squad_metrics import squad_evaluate

from covid19_qa.dataset import load_all_annotated_instances
from covid19_qa.pipeline import DEFAULT_SORT_MODE, Instance, TYPE_SORT_MODE
from covid19_qa.qa import answer_from_instances


def evaluate_with_instances(instances: Iterator[Instance], qa_pipeline: Pipeline, min_score: Optional[float] = None,
                            sort_mode: TYPE_SORT_MODE = DEFAULT_SORT_MODE, batch_size: int = 32,
                            threads: int = 1) -> Mapping[str, Number]:
    instances = list(instances)
    answers = answer_from_instances(instances, qa_pipeline, remove_empty_answers=False, min_score=min_score,
                                    sort_mode=sort_mode, batch_size=batch_size, threads=threads)
    predictions = {a.instance.qas_id: a.text for a in answers}
    no_answer_probs = {a.instance.qas_id: a.null_answer.sort_score for a in answers}
    return squad_evaluate(instances, predictions, no_answer_probs=no_answer_probs)


def evaluate_with_all_annotated_instances(qa_pipeline: Pipeline, merge_all_texts: bool = False,
                                          min_score: Optional[float] = None,
                                          sort_mode: TYPE_SORT_MODE = DEFAULT_SORT_MODE,
                                          batch_size: int = 32, threads: int = 1) -> Mapping[str, Number]:
    instances = load_all_annotated_instances()

    if merge_all_texts:
        instances = list(instances)

        all_texts = "\n\n".join(instance.context_text for instance in instances)

        some_instance = instances[0]
        reference_instance = Instance(qas_id=some_instance.qas_id, question_text=some_instance.question_text,
                                      context_text=all_texts, answer_text=some_instance.answer_text,
                                      start_position_character=None, is_impossible=some_instance.is_impossible,
                                      answers=some_instance.answers, title=some_instance.title)

        for instance in instances:
            instance.context_text = all_texts

            instance.start_position = 0
            instance.end_position = 0

            instance.doc_tokens = reference_instance.doc_tokens
            instance.char_to_word_offset = reference_instance.char_to_word_offset

            for answer_dict in instance.answers:
                answer_dict["answer_start"] = None

    return evaluate_with_instances(instances, qa_pipeline, min_score=min_score, sort_mode=sort_mode,
                                   batch_size=batch_size, threads=threads)
