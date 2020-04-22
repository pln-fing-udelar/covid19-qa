from flask import request
from flask_restx import Resource

from covid19_qa.qa import answer_question_from_all_docs
from . import custom_response
from .. import ns_covid_qa
from .. import qa_pipeline

@ns_covid_qa.route('/question')
class Covid19(Resource):
    def post(self):
        """
        Make a question
        """
        json_data = request.get_json(force=True)
        try:
            question = json_data.get('question')
            qa_answers = answer_question_from_all_docs(question, qa_pipeline)
            responses = []
            for answer in qa_answers:
                responses.append(
                    {
                        'title': 'Not implemented',
                        'context': answer.instance.context_text,
                        'answer': answer.text,
                        'answer_start_index': answer.start,
                        'answer_end_index': answer.start + len(answer.text),
                        'date': None, # TODO: Add in the instance class the date. Maybe include it in the source
                        'source': {} # TODO: Add in the instance class the source. Add the date inside?
                    }
                )
            return responses
        except Exception as e:
            return custom_response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, 400)