import logging
from dataclasses import dataclass

import marshmallow_dataclass
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Resource

from .. import ns_covid_qa
from ..views import custom_response

log = logging.getLogger('covid19-api')


# TODO: Quitar estas definiciones e importar correctamente el modulo del Modelo
@dataclass
class Answer:
    text_id: str
    text: str
    in_context: str
    score: float


@dataclass
class Question:
    text: str


@dataclass
class Status:
    version: str
    status: str


@dataclass
class Feedback:
    question_text: str
    answer_text_id: str
    answer_text: str
    answer_score: float
    feedback: bool


AnswerSchema = marshmallow_dataclass.class_schema(Answer)
answer_schema = AnswerSchema()
answer_list_schema = AnswerSchema(many=True)
QuestionSchema = marshmallow_dataclass.class_schema(Question)
question_schema = QuestionSchema()
question_list_schema = QuestionSchema(many=True)
StatusSchema = marshmallow_dataclass.class_schema(Status)
status_schema = StatusSchema()
FeedbackSchema = marshmallow_dataclass.class_schema(Feedback)
feedback_list_schema = FeedbackSchema(many=True)


@ns_covid_qa.route('/')
class Covid19(Resource):

    @responds(schema=status_schema, api=ns_covid_qa, status_code=200)
    def get(self):
        """
        Obtener versión y estado actual del Modelo de QA
        """
        # TODO: Obtener versión y estado del modelo
        return None

    @accepts(schema=question_schema, api=ns_covid_qa)
    @responds(schema=answer_list_schema, api=ns_covid_qa, status_code=200)
    def post(self):
        """
        Obtener lista de posibles respuestas a una pregunta
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return custom_response({'message': 'No se encontró la pregunta'}, 400)
        try:
            # Validate and deserialize input
            question = question_schema.load(json_data)
            # TODO: Obtener posibles respuestas del modelo
            return []
        except Exception as e:
            return custom_response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, 400)


@ns_covid_qa.route('/preguntas-frecuentes')
class Covid19(Resource):

    @responds(schema=question_list_schema, api=ns_covid_qa, status_code=200)
    def get(self):
        """
        Obtener lista de preguntas frecuentes
        """
        # TODO: Obtener lista de preguntas frecuentes
        return []


@ns_covid_qa.route('/feedback')
class Covid19(Resource):

    @accepts(schema=feedback_list_schema, api=ns_covid_qa)
    @responds(api=ns_covid_qa, status_code=200)
    def post(self):
        """
        Recibir una lista con feedback para un grupo de respuestas
        """
        # TODO: Guardar feedback y contador de preguntas
        return []
