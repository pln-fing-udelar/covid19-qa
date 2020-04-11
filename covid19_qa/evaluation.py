from dataclasses import replace
from numbers import Number
from typing import Iterator, Mapping, Optional

from transformers import Pipeline
from transformers.data.metrics.squad_metrics import squad_evaluate

from covid19_qa.dataset import load_all_annotated_instances
from covid19_qa.pipeline import Answer, DEFAULT_SORT_MODE, Instance, TYPE_SORT_MODE
from covid19_qa.qa import answer_from_instances, answer_question_from_all_docs


def evaluate_answers(instances: Iterator[Instance], answers: Iterator[Answer]) -> Mapping[str, Number]:
    instances, answers = list(instances), list(answers)
    predictions = {a.instance.qas_id: a.text for a in answers}
    no_answer_probs = {a.instance.qas_id: a.null_answer.sort_score for a in answers}
    return squad_evaluate(instances, predictions, no_answer_probs=no_answer_probs)


def evaluate_with_instances(instances: Iterator[Instance], qa_pipeline: Pipeline, min_score: Optional[float] = None,
                            sort_mode: TYPE_SORT_MODE = DEFAULT_SORT_MODE, batch_size: int = 32,
                            threads: int = 1) -> Mapping[str, Number]:
    instances = list(instances)
    answers = answer_from_instances(instances, qa_pipeline, remove_empty_answers=False, min_score=min_score,
                                    sort_mode=sort_mode, batch_size=batch_size, threads=threads)
    return evaluate_answers(instances, answers)


def evaluate_with_all_annotated_instances(qa_pipeline: Pipeline, search_all_texts: bool = False,
                                          min_score: Optional[float] = None,
                                          sort_mode: TYPE_SORT_MODE = DEFAULT_SORT_MODE,
                                          batch_size: int = 32, threads: int = 1) -> Mapping[str, Number]:
    instances = load_all_annotated_instances()

    if search_all_texts:
        instances = list(instances)

        answers = []
        for instance in instances:
            question_answers = answer_question_from_all_docs(instance.question_text, qa_pipeline, top_k=1,
                                                             remove_empty_answers=False, min_score=min_score,
                                                             sort_mode=sort_mode, batch_size=batch_size,
                                                             threads=threads)
            question_answers = list(question_answers)

            assert len(question_answers) == 1

            answer = replace(question_answers[0], instance=instance)
            answers.append(answer)

        return evaluate_answers(instances, answers)
    else:
        return evaluate_with_instances(instances, qa_pipeline, min_score=min_score, sort_mode=sort_mode,
                                       batch_size=batch_size, threads=threads)
