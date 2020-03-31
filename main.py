#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass
from typing import Iterable, Iterator, Tuple
from xml.dom import minidom

from nltk.tokenize import sent_tokenize
from transformers import Pipeline, pipeline

PATH_DATA = 'data'
PATH_MODEL_FOLDER = 'model'


@dataclass
class Answer:
    text_id: str
    text: str
    in_context: str
    score: float


def generate_context_snippets(path_data: str, docs: Iterator[str], snippet_size: int) -> Iterator[Tuple[str, str]]:
    """A snippet is a set of snippet_size sentences."""
    context_snippets = []

    for text_id in docs:
        xml = minidom.parse(os.path.join(path_data, text_id + ".xml"))
        article = xml.getElementsByTagName('article')
        article_text = article[0].firstChild.nodeValue
        sentences = sent_tokenize(article_text)
        offset = len(sentences) // snippet_size
        remainder = len(sentences) % snippet_size

        for x in range(offset):
            snippet_text = ' '.join(
                map(str, sentences[x * snippet_size:(x + 1) * snippet_size]))
            context_snippets.append((snippet_text, text_id))

        if remainder > 0:
            snippet_text = ' '.join(
                map(str, sentences[offset * snippet_size:offset * snippet_size + remainder]))
            context_snippets.append((snippet_text, text_id))

    return context_snippets


def highlight_answer(text_id: str, context: str, question: str, qa_pipeline: Pipeline) -> Answer:
    """Given a context and a question, returns a pair (highlighted answer, score)"""
    result = qa_pipeline({"question": question, "context": context}, version_2_with_negative=True)
    if len(result['answer']) == 0:
        return Answer(text_id=text_id, text="", in_context="", score=result["score"])
    else:
        return Answer(text_id=text_id, text=result["answer"], score=result["score"],
                      in_context=context[:result['start']] + '{{' + result['answer'] + '}}' + context[result['end']:])


def rank_answers(answers: Iterable[Answer], clean_mode: bool) -> Iterator[Answer]:
    """Each element in 'answers' has a score. Returns a list sorted in descending order.
    In clean_mode, empty answers won't be returned.
    """
    if clean_mode:
        answers = list(filter(lambda elem: elem.text != "", answers))

    return sorted(answers, reverse=True, key=lambda x: x.score)


def qa(path_data: str, question: str) -> Iterator[Answer]:
    """Given a dataset with multiple texts, returns the top 10 most confident paragraphs with the highlighted answer.
    Highlighted text *like this*.
    """
    qa_pipeline = pipeline("question-answering", model=PATH_MODEL_FOLDER, config=PATH_MODEL_FOLDER,
                           tokenizer=PATH_MODEL_FOLDER)

    docs = [file_name[:-4] for file_name in os.listdir(path_data) if file_name.endswith(".xml")]
    answers = [highlight_answer(text_id, context, question, qa_pipeline)
               for context, text_id in generate_context_snippets(path_data, docs, snippet_size=5)]

    return rank_answers(answers, True)


def main() -> None:
    for answer in qa(PATH_DATA, "¿Qué criticó Da Silveira?"):
        print("** Text id:", answer.text_id)
        print("** Answer:", answer.text)
        print("** Score:", answer.score)
        print("** In context:")
        print(answer.in_context)
        print()


if __name__ == "__main__":
    main()
