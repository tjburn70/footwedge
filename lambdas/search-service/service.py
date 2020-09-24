import elasticsearch
from fastapi import HTTPException


class SearchService:

    def __init__(self, es_client: elasticsearch.Elasticsearch):
        self.es_client = es_client

    # def get_index(self, index: str):
    #     try:
    #         results = self.es_client.indices.get(index=index)
    #         return results
    #     except elasticsearch.exceptions.NotFoundError as exc:
    #         raise HTTPException(status_code=404, detail=exc.info)

    def get_indices(self):
        results = self.es_client.cat.indices()
        return results

    def create_index(self, index: str, body: dict = None):
        try:
            resp = self.es_client.indices.create(
                index=index,
                body=body,
            )
            return resp
        except elasticsearch.exceptions.RequestError as req_exc:
            raise HTTPException(status_code=400, detail=req_exc.info)

    def delete_index(self, index: str):
        try:
            resp = self.es_client.indices.delete(
                index=index,
            )
            return resp
        except elasticsearch.exceptions.NotFoundError as exc:
            raise HTTPException(status_code=404, detail=exc.info)

    def full_text_search(self, index: str, field: str, text: str):
        body = {
            'query': {
                'match': {
                    field: {'query': text}
                }
            }
        }
        results = self.es_client.search(
            index=index,
            body=body
        )
        return results

    def full_text_search_multi(self, index: str, text: str, fields: list = None):
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
        results = self.es_client.search(
            index=index,
            body=body
        )
        return results

    def get_document(self, index: str, document_id: str):
        try:
            results = self.es_client.get(index=index, id=document_id)
        except elasticsearch.exceptions.NotFoundError as exc:
            raise HTTPException(status_code=404, detail=exc.info)
        return results

    def get_all_documents(self, index: str):
        body = {"query": {"match_all": {}}}
        results = self.es_client.search(body=body, index=index)
        return results.get('hits')

    def add_document(self, index: str, payload: dict, document_id: str = None):
        if not self.es_client.indices.exists(index=index):
            error_message = f"Index: '{index}' not found"
            raise HTTPException(status_code=404, detail=error_message)
        if self.es_client.exists(index=index, id=document_id):
            error_message = f"The document with id: {document_id} already exists in the index: {index}"
            raise HTTPException(status_code=409, detail=error_message)

        resp = self.es_client.index(index=index, id=document_id, body=payload)
        return resp

    def add_to_nested_property(self, index: str, document_id: str, nested_property: str, nested_property_body: dict):
        nested_property_singular = nested_property.rstrip("s")
        print("nested_property_singular: ", nested_property_singular)
        script = f"ctx._source.{nested_property}.add(params.{nested_property_singular})"
        body = {
            "script": {
                "source": script,
                "params": {
                    nested_property_singular: nested_property_body
                }
            }
        }
        resp = self.es_client.update(
            index=index,
            id=document_id,
            body=body
        )
        print(type(resp))
        print(resp)
        return resp

    def delete_document(self, index: str, document_id: str):
        pass
