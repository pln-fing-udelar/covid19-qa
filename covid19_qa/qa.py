# -*- coding: utf-8 -*-
import heapq
import logging
import time
from typing import Iterator, Optional

from transformers import Pipeline

from covid19_qa.dataset import all_doc_ids, Document, load_documents
from covid19_qa.pipeline import Answer, Instance

logger = logging.getLogger(__name__)


def answer_from_instances(instances: Iterator[Instance], qa_pipeline: Pipeline, top_k: Optional[int] = None,
                          top_k_per_instance: int = 1, remove_empty_answers: bool = True, batch_size: int = 32,
                          threads: int = 1) -> Iterator[Answer]:
    start_time = time.time()

    answers = qa_pipeline(instances, version_2_with_negative=True, topk=top_k_per_instance, batch_size=batch_size,
                          threads=threads)

    if remove_empty_answers:
        answers = (a for a in answers if a.text)

    # `nlargest` needs a `Sized` `Iterable` and `sorted` needs an `Iterable`.
    answers = list(answers)

    # We need to measure here, because before the answers may not have been generated yet.
    logger.info(f"Model time: {time.time() - start_time:6.1f}s")

    if top_k is None:
        return sorted(answers, reverse=True, key=lambda a: a.sort_key)
    else:
        return heapq.nlargest(top_k, answers, key=lambda a: a.sort_key)


def answer_question_from_documents(documents: Iterator[Document], question: str, qa_pipeline: Pipeline,
                                   top_k: Optional[int] = None, top_k_per_instance: int = 1,
                                   remove_empty_answers: bool = True, batch_size: int = 32,
                                   threads: int = 1) -> Iterator[Answer]:
    instances = (Instance(qas_id=doc.id, question_text=question, context_text=doc.text, answer_text=None,
                          start_position_character=None, title=question)
                 for doc in documents)
    return answer_from_instances(instances, qa_pipeline, top_k=top_k, top_k_per_instance=top_k_per_instance,
                                 remove_empty_answers=remove_empty_answers, batch_size=batch_size, threads=threads)


def answer_question_from_doc_ids(doc_ids: Iterator[str], question: str, qa_pipeline: Pipeline,
                                 top_k: Optional[int] = None, top_k_per_instance: int = 1,
                                 remove_empty_answers: bool = True, snippet_size: int = 5, batch_size: int = 32,
                                 threads: int = 1) -> Iterator[Answer]:
    snippets = load_documents(doc_ids=doc_ids, snippet_size=snippet_size)
    return answer_question_from_documents(snippets, question, qa_pipeline, top_k=top_k,
                                          top_k_per_instance=top_k_per_instance,
                                          remove_empty_answers=remove_empty_answers, batch_size=batch_size,
                                          threads=threads)


def answer_question_from_all_docs(question: str, qa_pipeline: Pipeline, top_k: Optional[int] = None,
                                  top_k_per_instance: int = 1, remove_empty_answers: bool = True, snippet_size: int = 5,
                                  batch_size: int = 32, threads: int = 1) -> Iterator[Answer]:
    doc_ids = all_doc_ids()
    return answer_question_from_doc_ids(doc_ids, question, qa_pipeline, top_k=top_k,
                                        top_k_per_instance=top_k_per_instance,
                                        remove_empty_answers=remove_empty_answers, snippet_size=snippet_size,
                                        batch_size=batch_size, threads=threads)
