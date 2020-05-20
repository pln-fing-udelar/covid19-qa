import os
from typing import Any, Dict, Iterator, Mapping

from elasticsearch import Elasticsearch

from covid19_qa.pipeline import Instance, Document

ES_HOST = os.getenv("ES_HOST")
es = Elasticsearch([{"host": ES_HOST, "port": os.environ["ES_PORT"]}]) if ES_HOST else None

DEFAULT_ES_QUERY_CONF = [
    {"operator": "and", "minimum_should_match": 80, "fuzziness": 1, "boost": 3},
    {"operator": "and", "minimum_should_match": 60, "fuzziness": 1, "boost": 4},
    {"operator": "or", "minimum_should_match": 80, "fuzziness": 1, "boost": 3},
    {"operator": "or", "minimum_should_match": 50, "fuzziness": 1, "boost": 1},
]


def get_match_query_from_conf(query: str, text_field: str, conf: Dict) -> Dict:
    return {
        "match": {
            text_field: {
                "query": query,
                "operator": conf.get("operator"),
                "minimum_should_match": f"{conf.get('minimum_should_match')}%",
                "fuzziness": conf.get("fuzziness"),
                "boost": conf.get("boost")
            }
        }
    }


def search_query_string(query: str, index_pattern: str = "covid*", size: int = 20, fragments: int = 2,
                        fragment_size: int = 1500, text_field: str = "article_text",
                        es_query_configurations: Iterator[Dict] = DEFAULT_ES_QUERY_CONF) -> Iterator[Mapping[str, Any]]:
    es_query = query.replace("?", "").replace("¿", "")
    return es.search(
        index=index_pattern,
        body={
            "from": 0,
            "size": size,
            "query": {
                "bool": {
                    "should": [
                        get_match_query_from_conf(es_query, text_field, conf) for conf in es_query_configurations
                    ]
                }
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
