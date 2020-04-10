#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
import time

from transformers import Pipeline

from covid19_qa.argparse_with_defaults import ArgumentParserWithDefaults
from covid19_qa.pipeline import create_qa_pipeline
from covid19_qa.qa import answer_question_from_all_docs
from covid19_qa.evaluation import evaluate_with_all_annotated_instances

logger = logging.getLogger(__name__)


def _show_answers(args: argparse.Namespace, qa_pipeline: Pipeline, question: str) -> None:
    answers = answer_question_from_all_docs(question, qa_pipeline, top_k=args.top_k,
                                            top_k_per_instance=args.top_k_per_document, batch_size=args.batch_size,
                                            threads=args.threads)
    for answer in answers:
        print("** Doc ID:", answer.instance.qas_id)
        print("** Answer:", answer.text)
        print(f"** Score: {answer.score * 100:3.0f}%")
        print("** In context:")
        print(answer.in_context)
        print()


def _interact(args: argparse.Namespace, qa_pipeline: Pipeline) -> None:
    print("Write a question or 'exit'.")
    question = input("Question: ")
    while question.lower() != "exit":
        _show_answers(args, qa_pipeline, question)
        question = input("Question: ")


def _evaluate(args: argparse.Namespace, qa_pipeline: Pipeline) -> None:
    results = evaluate_with_all_annotated_instances(qa_pipeline, batch_size=args.batch_size, threads=args.threads)
    for k, v in results.items():
        if isinstance(v, float):
            print(f"{k}: {v:5.1f}")
        else:
            print(f"{k}: {v}")


def _try(args: argparse.Namespace, qa_pipeline: Pipeline) -> None:
    question = "¿Qué criticó Da Silveira?"
    print("Question:", question)
    print()
    _show_answers(args, qa_pipeline, question=question)


def _parse_args() -> argparse.Namespace:
    parser = ArgumentParserWithDefaults()
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--device", type=int, default=-1,
                        help="device where the model is run. -1 is CPU, otherwise it's the GPU ID")
    parser.add_argument("--threads", type=int, default=4,
                        help="number of threads used to convert the instances to features")
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--top-k-per-document", type=int, default=5)
    parser.add_argument("-v", "--verbose", action="store_true")

    subparsers = parser.add_subparsers(title="mode", description="Run mode. Use 'trial' to just try things out. "
                                                                 "Use 'evaluation' to measure the performance. "
                                                                 "Use 'interactive' to write your own questions "
                                                                 "and see the answers.")

    interact_subparser = subparsers.add_parser("interact")
    interact_subparser.set_defaults(func=_interact)

    evaluate_subparser = subparsers.add_parser("evaluate")
    evaluate_subparser.set_defaults(func=_evaluate)

    try_subparser = subparsers.add_parser("try")
    try_subparser.set_defaults(func=_try)

    return parser.parse_args()


def _set_up_logging(verbose: bool = False) -> None:
    logging_level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", level=logging_level)


def main() -> None:
    start_time = time.time()

    args = _parse_args()

    _set_up_logging(verbose=args.verbose)

    qa_pipeline = create_qa_pipeline(device=args.device)

    func = getattr(args, "func", _try)
    func(args, qa_pipeline)

    logger.info(f"Time elapsed: {time.time() - start_time:6.1f}s")


if __name__ == "__main__":
    main()
