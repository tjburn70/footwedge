from elasticsearch import Elasticsearch

from api.config import ELASTICSEARCH_URL

es = Elasticsearch(hosts=[ELASTICSEARCH_URL])


def add_to_index(index, index_id, data, schema):
    payload = schema.loads(data)
    es.index(index=index, id=index_id, body=payload)


def remove_from_index(index, index_id):
    es.delete(index=index, id=index_id)


def full_text_search(index: str, field: str, text: str):
    body = {
        'query': {
            'match': {
                field: {'query': text}
            }
        }
    }
    results = es.search(
        index=index,
        body=body
    )

    return results


def full_text_search_multi(index: str, text: str, fields: list = None):
    if not fields:
        fields = ['*']

    body = {
        'query': {
            'multi_match': {
                'query': text,
                'fields': fields,
            }
        }
    }

    results = es.search(
        index=index,
        body=body
    )

    return results
