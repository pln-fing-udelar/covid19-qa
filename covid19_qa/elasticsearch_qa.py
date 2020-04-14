from elasticsearch import Elasticsearch
from typing import Iterator

from covid19_qa.pipeline import Instance

# FIXME: The elasticsearch configuration should be a setting
es = Elasticsearch([{'host': '0.0.0.0', 'port': 19200}])

def serch_query_string(query, index_pattern='covid*', size=10, fragments=1,
                       fragment_size=200,
                       text_field='article_text',):
    return es.search(
        index=index_pattern,
        body={
            'from': 0,
            'size': size,
            'query': {
                'query_string' : {
                    'query' : query,
                    'default_field' : text_field,
                    'minimum_should_match': 1
                }
            },
            'highlight': {
                'fields': {
                    '*': {}
                },
                'number_of_fragments' : fragments,
                'fragment_size': fragment_size,
                'pre_tags': [''],
                'post_tags': ['']
            },
        })['hits']['hits']

def get_instances_from_es(question: str) -> Iterator[Instance]:
    instances = []
    for result in serch_query_string(question):
        for fragment in result['highlight']['article_text']:
            instances.append(
                Instance(
                    qas_id=result['_id'],
                    question_text=question,
                    context_text=fragment,
                    answer_text=None,
                    start_position_character=None, 
                    title=question)
            )
    return instances