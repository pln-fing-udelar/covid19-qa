#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
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
    """
    Returns a list of (snippet, text_id)
    A snippet is a set of snippet_size sentences.
    """
    context_snippets = []

    for text_id in docs:
        xml = minidom.parse(os.path.join(path_data, text_id + ".xml"))
        article = xml.getElementsByTagName('article')
        article_text = article[0].firstChild.nodeValue
        sentences = sent_tokenize(article_text)

        for i in range(0, len(sentences), snippet_size):
            snippet_text = ' '.join(map(str, sentences[i:i+snippet_size]))
            context_snippets.append((snippet_text, text_id))

    return context_snippets


def highlight_answers(context_textid_list: Iterable[Tuple[str, str]], question: str, qa_pipeline: Pipeline) -> Iterator[Answer]:
    """Given a context and a question, returns a pair (highlighted answer, score)"""
    contexts, text_ids = list(zip(*context_textid_list))
    questions = [{"question": question, "context": c} for c in contexts]
    results = qa_pipeline(questions, version_2_with_negative=True)

    answers = []
    for result, context, text_id in zip(results, contexts, text_ids):
        if len(result['answer']) == 0:
            answers.append(Answer(text_id=text_id, text="", in_context="",
                                  score=result["score"]))
        else:
            answers.append(Answer(text_id=text_id, text=result["answer"],
                                  score=result["score"], 
                                  in_context=context[:result['start']] 
                                  + '{{' + result['answer'] + '}}' 
                                  + context[result['end']:]))
    return answers


def rank_answers(answers: Iterable[Answer], clean_mode: bool) -> Iterator[Answer]:
    """Each element in 'answers' has a score. Returns a list sorted in descending order.
    In clean_mode, empty answers won't be returned.
    """
    if clean_mode:
        answers = list(filter(lambda elem: elem.text != "", answers))

    return sorted(answers, reverse=True, key=lambda x: x.score)



def qa(qa_pipeline: Pipeline, question: str) -> Iterator[Answer]:
    """
    """
    docs = [file_name[:-4] for file_name in os.listdir(PATH_DATA) 
                            if file_name.endswith(".xml")]
    context_textid_list = generate_context_snippets(PATH_DATA, docs, snippet_size=5) 
    answers = highlight_answers(context_textid_list, question, qa_pipeline)
    return rank_answers(answers, True)




def main() -> None:
    start = time.time()
    qa_pipeline = pipeline("question-answering", model=PATH_MODEL_FOLDER,
                    config=PATH_MODEL_FOLDER, tokenizer=PATH_MODEL_FOLDER)
    for answer in qa(qa_pipeline, "¿Qué criticó Da Silveira?"):
        print("** Text id:", answer.text_id)
        print("** Answer:", answer.text)
        print("** Score:", answer.score)
        print("** In context:")
        print(answer.in_context)
        print()
    end = time.time()
    print('Time elapsed: ',end - start)


if __name__ == "__main__":
    main()
