from typing import Optional

import uvicorn
from fastapi import FastAPI, Body
from elasticsearch import Elasticsearch

from service import SearchService


SEARCH_ENGINE_URL = "http://localhost:9200"
app = FastAPI()
es_client = Elasticsearch(hosts=[SEARCH_ENGINE_URL])


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
async def search_index(index: str, q: str, field: Optional[str] = None):
    search_service = SearchService(es_client=es_client)
    if field:
        results = search_service.full_text_search(
            index=index,
            text=q,
            field=field,
        )
    else:
        results = search_service.full_text_search_multi(
            index=index,
            text=q,
        )

    return results


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


if __name__ == "__main__":
    uvicorn.run('api:app', host='0.0.0.0', port=8001, reload=True)
