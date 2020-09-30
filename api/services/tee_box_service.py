from http import HTTPStatus

from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.repositories.tee_box_repository import TeeBoxRepository
from api.schemas import TeeBoxSchema


class TeeBoxService:

    def __init__(self, repo: TeeBoxRepository, schema: TeeBoxSchema):
        self._tee_box_repo = repo
        self._tee_box_schema = schema

    def get(self, _id: int) -> Response:
        tee_box = self._tee_box_repo.get(_id)
        result = self._tee_box_schema.dump(tee_box)
        response_body = {
            'status': 'success',
            'result': result.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_all(self) -> Response:
        tee_boxes = self._tee_box_repo.get_all()
        results = self._tee_box_schema.dump(tee_boxes, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_by_golf_course_id(self, golf_course_id: int):
        tee_boxes = self._tee_box_repo.get_by_golf_course_id(golf_course_id=golf_course_id)
        results = self._tee_box_schema.dump(tee_boxes, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def add(self, golf_course_id: int, payload: dict) -> Response:
        payload['golf_course_id'] = golf_course_id
        try:
            tee_box_data = self._tee_box_schema.load(payload).data
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        tee_box = self._tee_box_repo.create(data=tee_box_data)
        tee_box_id = tee_box.id
        response_body = {
            'status': 'success',
            'message': f"Tee Box: '{tee_box.tee_color}' was successfully added",
            'uri': f'/api/golf-courses/{golf_course_id}/tee-boxes/{tee_box_id}',
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)