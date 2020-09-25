import os
from typing import List

import uvicorn
from fastapi import FastAPI, Body, Query
from elasticsearch import Elasticsearch

from service import SearchService


SEARCH_ENGINE_URI = os.environ.get('SEARCH_ENGINE_URI')
app = FastAPI()
es_client = Elasticsearch(hosts=[SEARCH_ENGINE_URI])


@app.get('/health')
async def root():
    return "Welcome to Search Service"


@app.get('/')
async def get_all_indexes():
    return SearchService(es_client=es_client).get_indices()


@app.post('/{index}')
async def create_index(index: str, body: dict = Body(...)):
    return SearchService(es_client=es_client).create_index(index=index, body=body)


@app.delete('/{index}')
async def delete_index(index: str):
    return SearchService(es_client=es_client).delete_index(index=index)


# @app.get('/{index}')
# async def get_index(index: str):
#     return SearchService(es_client=es_client).get_index(index=index)


@app.get('/{index}')
async def search_index(index: str, q: str, query_type: str, field: List[str] = Query(...)):
    search_service = SearchService(es_client=es_client)
    return search_service.full_text_search(
        index=index,
        query_type=query_type,
        text=q,
        fields=field,
    )


@app.get('/{index}/_doc')
async def get_all_documents(index: str):
    return SearchService(es_client=es_client).get_all_documents(index=index)


@app.get('/{index}/_doc/{doc_id}')
async def get_document(index: str, doc_id: str):
    return SearchService(es_client=es_client).get_document(index=index, document_id=doc_id)


@app.put('/{index}/_doc')
async def add_document(index: str, payload: dict = Body(..., embed=True), _id: int = Body(..., embed=True)):
    search_service = SearchService(es_client=es_client)
    return search_service.add_document(
        index=index,
        payload=payload,
        document_id=_id,
    )


@app.put('/{index}/_doc/{doc_id}/_update/{nested_property}')
async def update_doc_nested_property(index: str, doc_id: str, nested_property: str, payload: dict = Body(...)):
    search_service = SearchService(es_client=es_client)
    return search_service.add_to_nested_property(
        index=index,
        document_id=doc_id,
        nested_property=nested_property,
        nested_property_body=payload,
    )


@app.delete('/{index}/_doc/{doc_id}')
async def delete_document(index: str, doc_id: str):
    return SearchService(es_client=es_client).delete_document(index=index, document_id=doc_id)


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8001, reload=True)
