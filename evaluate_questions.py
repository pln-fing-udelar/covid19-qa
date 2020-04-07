#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from xml.dom import minidom

from nltk.tokenize import RegexpTokenizer
from transformers import Pipeline, pipeline

PATH_MODEL_FOLDER = 'model'

tokenizer = RegexpTokenizer(r'\w+')

def calculate_f1(expected,candidate):
    expected_tokens = set(t.lower() for t in tokenizer.tokenize(expected))
    candidate_tokens = set(t.lower() for t in tokenizer.tokenize(candidate))
    intersection = expected_tokens & candidate_tokens
    if len(expected_tokens) == 0:
        if len(candidate_tokens) == 0:
            return 1
        else:
            return 0
    elif len(candidate_tokens) == 0:
        return 0
    p = len(intersection) / len(expected_tokens)
    r = len(intersection) / len(candidate_tokens)
    if p+r == 0:
        return 0
    return 2*p*r / (p+r)

def load_snippets(file_name):
    snippets = []
    doc = minidom.parse(file_name)
    for snippet in doc.getElementsByTagName('snippet'):
        questions = []
        for question in snippet.getElementsByTagName('question'):
            if len(question.attributes['q'].value) > 0:
                questions.append((question.attributes['q'].value,question.attributes['a'].value))
        text = snippet.getElementsByTagName('text')[0].firstChild.nodeValue
        snippets.append((text,questions))
    return snippets

def main() -> None:
    snippets = load_snippets(sys.argv[1])

    qa_pipeline = pipeline("question-answering", model=PATH_MODEL_FOLDER, config=PATH_MODEL_FOLDER, tokenizer=PATH_MODEL_FOLDER)
    num_questions = 0
    exact_match = 0
    f1 = 0
    for text,questions in snippets:
        print(text)
        for q,a in questions:
            num_questions += 1
            result = qa_pipeline({"question": q, "context": text}, version_2_with_negative=True)
            print("Question: ",q)
            print("Expected: ",a)
            print("Candidate: ",result)
            c = result['answer']
            if result['score'] < 0.5:
                c = ''
            if a == c:
                exact_match += 1
            f1 += calculate_f1(a,c)
    print("EM: ",exact_match / num_questions)
    print("F1: ",f1 / num_questions)

if __name__ == "__main__":
    main()
