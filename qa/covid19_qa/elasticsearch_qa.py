import os
from typing import Any, Iterator, Mapping

from elasticsearch import Elasticsearch

from covid19_qa.pipeline import Instance, Document

ES_HOST = os.getenv("ES_HOST")
es = Elasticsearch([{"host": ES_HOST, "port": os.environ["ES_PORT"]}]) if ES_HOST else None


def search_query_string(query: str, index_pattern: str = "covid*", size: int = 10, fragments: int = 1,
                        fragment_size: int = 700, text_field: str = "article_text") -> Iterator[Mapping[str, Any]]:
    return es.search(
        index=index_pattern,
        body={
            "from": 0,
            "size": size,
            "query": {
                "query_string": {
                    "query": query,
                    "default_field": text_field,
                    "minimum_should_match": 1,
                },
            },
            "highlight": {
                "fields": {
                    "*": {},
                },
                "number_of_fragments": fragments,
                "fragment_size": fragment_size,
                "pre_tags": [""],
                "post_tags": [""],
            },
        })["hits"]["hits"]


def get_instances_from_es(question: str) -> Iterator[Instance]:
    for result in search_query_string(question):
        document_dict = result["_source"]
        # We don't want to return the whole text of each document, so we just set it to null.
        document = Document(id=document_dict["article_id"], text=None, title=document_dict["article_title"],
                            source=document_dict["article_src"], date=document_dict["article_date"],
                            url=document_dict["article_url"])
        for fragment in result["highlight"]["article_text"]:
            yield Instance(qas_id=result["_id"], question_text=question, context_text=fragment, answer_text=None,
                           start_position_character=None, document=document)
