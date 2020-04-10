from numbers import Number
from typing import Mapping

from transformers import Pipeline
from transformers.data.metrics.squad_metrics import squad_evaluate

from covid19_qa.dataset import load_all_annotated_instances
from covid19_qa.qa import answer_from_instances


def evaluate_with_all_annotated_instances(qa_pipeline: Pipeline, batch_size: int = 32,
                                          threads: int = 1) -> Mapping[str, Number]:
    instances = list(load_all_annotated_instances())
    answers = answer_from_instances(instances, qa_pipeline, remove_empty_answers=False, batch_size=batch_size,
                                    threads=threads)
    predictions = {a.instance.qas_id: a.text for a in answers}
    no_answer_probs = {a.instance.qas_id: a.null_sort_key for a in answers}
    return squad_evaluate(instances, predictions, no_answer_probs=no_answer_probs)
