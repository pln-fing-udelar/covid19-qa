#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from transformers import pipeline
from main_batch import qa, PATH_MODEL_FOLDER


def main() -> None:

    qa_pipeline = pipeline("question-answering", model=PATH_MODEL_FOLDER,
                    config=PATH_MODEL_FOLDER, tokenizer=PATH_MODEL_FOLDER)
    
    print("\nWrite a question or 'exit'.")
    question = input('Question: ')
    while question.lower() not in ['exit','salir']:
        start = time.time()
        for answer in qa(qa_pipeline, question):
            print("** Text id:", answer.text_id)
            print("** Answer:", answer.text)
            print("** Score:", answer.score)
            print("** In context:")
            print(answer.in_context)
            print()
        end = time.time()
        print('Time elapsed: ',end - start)
        question = input('Question: ')


if __name__ == "__main__":
    main()

