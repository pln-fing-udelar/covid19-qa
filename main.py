#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time

from transformers import Pipeline
from xml.dom import minidom  # noqa

from covid19_qa.argparse_with_defaults import ArgumentParserWithDefaults
from covid19_qa.qa import answer_question, create_qa_pipeline, calculate_f1, load_snippets


def _parse_args() -> argparse.Namespace:
    parser = ArgumentParserWithDefaults()
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--device", type=int, default=-1,
                        help="device where the model is run. -1 is CPU, otherwise it's the GPU ID")
    parser.add_argument("--mode", default="trial", choices=["interactive", "evaluation", "trial"],
                        help="Run mode. Use 'trial' to just try things out. "
                             "Use 'evaluation' to measure the performance. "
                             "Use 'interactive' to write your own questions and see the answers.")
    parser.add_argument("--snippet-size", type=int, default=5)
    parser.add_argument("--threads", type=int, default=4,
                        help="number of threads used to convert the instances to features")
    return parser.parse_args()


def _show_answers(args: argparse.Namespace, qa_pipeline: Pipeline, question: str) -> None:
    answers = answer_question(qa_pipeline, question, snippet_size=args.snippet_size, batch_size=args.batch_size,
                              threads=args.threads)
    for answer in answers:
        print("** Doc ID:", answer.snippet.doc_id)
        print("** Answer:", answer.text)
        print(f"** Score: {round(answer.score * 100)}%")
        print("** In context:")
        print(answer.in_context)
        print()


def main() -> None:
    start_time = time.time()

    args = _parse_args()

    qa_pipeline = create_qa_pipeline(device=args.device)

    if args.mode == "interactive":
        print("Write a question or 'exit'.")
        question = input("Question: ")
        while question.lower() not in {"exit", "salir"}:
            _show_answers(args, qa_pipeline, question)
            question = input("Question: ")
    elif args.mode == "evaluation":
        snippets = list(load_snippets("snippets.xml"))

        input_ = [{"question": question, "context": snippet.text}
                  for snippet, question_answer_pairs in snippets
                  for question, answer in question_answer_pairs]

        # answer_question(qa_pipeline, question, snippet_size=args.snippet_size, batch_size=args.batch_size,
        #                 threads=args.threads)
        results = qa_pipeline(input_, version_2_with_negative=True, batch_size=args.batch_size, threads=args.threads)

        num_questions = 0
        exact_match = 0
        f1 = 0
        for snippet, question_answer_pairs in snippets:
            print(snippet.text)
            for question, answer in question_answer_pairs:
                result = results[num_questions]
                num_questions += 1
                print("Question:", question)
                print("Expected:", answer)
                print("Candidate:", result)
                actual_answer = result["answer"]
                if result["score"] < 0.5:
                    actual_answer = ""
                if answer == actual_answer:
                    exact_match += 1
                f1 += calculate_f1(answer, actual_answer)
        print("EM:", exact_match / num_questions)
        print("F1:", f1 / num_questions)
    elif args.mode == "trial":
        _show_answers(args, qa_pipeline, question="¿Qué criticó Da Silveira?")
    else:
        raise ValueError(f"Unsupported mode: {args.mode}")

    print("Time elapsed:", time.time() - start_time)


if __name__ == "__main__":
    main()
