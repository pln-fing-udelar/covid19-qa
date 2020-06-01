# -*- coding: utf-8 -*-
import heapq
import logging
import time
from functools import lru_cache
from typing import Iterator, Optional

from transformers import Pipeline

from covid19_qa.dataset import all_doc_ids, get_instances_from_doc_ids
from covid19_qa.elasticsearch_qa import get_instances_from_es
from covid19_qa.pipeline import Answer, DEFAULT_SORT_MODE, Instance, TYPE_SORT_MODE

logger = logging.getLogger(__name__)


def answer_from_instances(instances: Iterator[Instance], qa_pipeline: Pipeline, top_k: Optional[int] = None,
                          top_k_per_instance: int = 1, remove_empty_answers: bool = True,
                          min_score: Optional[float] = None, sort_mode: TYPE_SORT_MODE = DEFAULT_SORT_MODE,
                          batch_size: int = 32, threads: int = 1) -> Iterator[Answer]:
    start_time = time.time()

    answers = qa_pipeline(instances, handle_impossible_answer=True, topk=top_k_per_instance, min_score=min_score,
                          sort_mode=sort_mode, batch_size=batch_size, threads=threads)

    if remove_empty_answers:
        answers = (a for a in answers if a.text)

    # `nlargest` needs a `Sized` `Iterable` and `sorted` needs an `Iterable`.
    answers = list(answers)

    # We need to measure here, because before the answers may not have been generated yet.
    logger.info(f"Model time: {time.time() - start_time:6.1f}s")

    if top_k is None:
        return sorted(answers, reverse=True, key=lambda a: a.sort_score)
    else:
        return heapq.nlargest(top_k, answers, key=lambda a: a.sort_score)


@lru_cache
def answer_question_from_all_docs(question: str, qa_pipeline: Pipeline, top_k: Optional[int] = None,
                                  top_k_per_instance: int = 1, remove_empty_answers: bool = True,
                                  min_score: Optional[float] = None, sort_mode: TYPE_SORT_MODE = DEFAULT_SORT_MODE,
                                  batch_size: int = 32, threads: int = 1, ignore_es: bool = False,
                                  es_query_conf: Iterator = None,
                                  ensure_question_marks: bool = True) -> Iterator[Answer]:
    question = question.strip()

    if ensure_question_marks:
        if not question.startswith("¿"):
            question = "¿" + question
        if not question.endswith("?"):
            question += "?"

    if ignore_es:
        instances = get_instances_from_doc_ids(all_doc_ids(), question)
    else:
        instances = get_instances_from_es(question, es_query_conf)
    return answer_from_instances(instances, qa_pipeline, top_k=top_k, top_k_per_instance=top_k_per_instance,
                                 remove_empty_answers=remove_empty_answers, min_score=min_score, sort_mode=sort_mode,
                                 batch_size=batch_size, threads=threads)
