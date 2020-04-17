import logging
from dataclasses import dataclass

import marshmallow_dataclass
from elasticsearch import Elasticsearch
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Resource

from .. import ns_test
from ..views import custom_response

log = logging.getLogger('covid19-test-api')
es = Elasticsearch([{'host': 'elasticsearch-covid', 'port': 9200}])

@dataclass
class Query:
    query: str
    index_pattern: str
    result_size: int
    number_of_fragments: int
    fragment_size: int
    text_field: str



QuerySchema = marshmallow_dataclass.class_schema(Query)
query_schema = QuerySchema()


@ns_test.route('/')
class Covid19(Resource):

    @accepts(schema=query_schema, api=ns_test)
    def post(self):
        """
        Obtener lista de posibles respuestas a una pregunta
        """
        json_data = request.get_json(force=True)
        if not json_data:
            return custom_response({'message': 'No se encontró la pregunta'}, 400)
        try:
            # Validate and deserialize input
            question = query_schema.load(json_data)
            return es.search(
                index=question.index_pattern,
                body={
                    "from": 0, "size": question.result_size,
                    "query": {
                        "query_string": {
                            "query": question.query,
                            "default_field": question.text_field,
                            "minimum_should_match": 1
                        }
                    },
                    "highlight": {
                        "fields": {
                            "*": {}
                        },
                        "number_of_fragments": question.number_of_fragments,
                        "fragment_size": question.fragment_size,
                        "pre_tags": ["<strong><u>"],
                        "post_tags": ["</u></strong>"]
                    }
                })['hits']['hits']
        except Exception as e:
            return custom_response({'error': 'Ha ocurrido un error: {}'.format(str(e))}, 400)

