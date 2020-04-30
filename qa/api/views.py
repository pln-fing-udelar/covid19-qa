import logging
import os
from typing import Any, Dict, List

import torch
from flask import json, Response
from flask import request
from flask_restx import Namespace, Resource

from covid19_qa.pipeline import create_qa_pipeline
from covid19_qa.qa import answer_question_from_all_docs

logger = logging.getLogger(__name__)


ANSWER_THREADS = os.getenv("ANSWER_THREADS", 1)
BATCH_SIZE = os.getenv("BATCH_SIZE", 32)
DEVICE = 0 if torch.cuda.is_available() else -1  # We can control this with CUDA_VISIBLE_DEVICES.
logger.info(f"PyTorch device set: {DEVICE}")
QA_PIPELINE = create_qa_pipeline(device=DEVICE)


def custom_response(response: Dict[str, Any], status_code: int):
    """Create a custom response."""
    return Response(mimetype="application/json", response=json.dumps(response), status=status_code)


api = Namespace("Covid19-QA", description="QA Operations")


@api.route("/question")
class Covid19(Resource):
    @staticmethod
    def post() -> List[Dict[str, Any]]:
        """Ask a question"""
        json_data = request.get_json(force=True)
        try:
            question = json_data.get("question")
            return [
                {
                    "title": answer.instance.document.title,
                    "context": answer.instance.context_text,
                    "answer": answer.text,
                    "answer_start_index": answer.start,
                    "answer_end_index": answer.end,
                    "date": answer.instance.document.date,
                    "source": answer.instance.document.source,
                    "url": answer.instance.document.url,
                } for answer in answer_question_from_all_docs(question, QA_PIPELINE, batch_size=BATCH_SIZE,
                                                              threads=ANSWER_THREADS)
            ]
        except Exception as e:
            return custom_response({"error": f"An error has occurred: {e}"}, 400)
