## Elasticsearch

### Ejecución

```bash
docker-compose up elasticsearch
```

El servicio `elasticsearch` es dependencia de logstash y jupyter y no es necesario levantarlo de manera independiente.

La API de Elasticsearch queda disponible en http://localhost:9200 desde el equipo host y desde los demás servicios de Docker como Logstash y Jupyter queda disponible en http://elasticsearch:9200

Desde Python se puede usar un cliente de la API:

```bash
pip install elasticsearch
```

Y para operar sobre Elasticsearch:

```python
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

def serch_query_string(query,
                         index_pattern='covid*',
                         size=10,
                         fragments=0,
                         text_field='article_text'):
    return es.search(
        index=index_pattern,
        body={
            "from": 0, "size": size,         
            "query": {
                    "query_string" : {
                        "query" : query,
                        "default_field" : text_field,
                        "minimum_should_match": 1
                    }
                },
             "highlight": {
                "fields": {
                    "*": {}
                },
                "number_of_fragments": fragments,
                 "fragment_size": 500,
                 "pre_tags":["<strong><u>"],
                 "post_tags":["</u></strong>"]
            }
        })['hits']['hits']
```
