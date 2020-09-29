from http import HTTPStatus

from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.repositories.hole_repository import HoleRepository
from api.schemas import HoleSchema


class HoleService:

    def __init__(self, repo: HoleRepository, schema: HoleSchema):
        self._hole_repo = repo
        self._hole_schema = schema

    def get(self, _id: int) -> Response:
        hole = self._hole_repo.get(_id)
        result = self._hole_schema.dump(hole)
        response_body = {
            'status': 'success',
            'result': result.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_all(self) -> Response:
        holes = self._hole_repo.get_all()
        results = self._hole_schema.dump(holes, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_by_tee_box_id(self, tee_box_id: int):
        holes = self._hole_repo.get_by_tee_box_id(tee_box_id=tee_box_id)
        results = self._hole_schema.dump(holes, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def add(self, golf_course_id: int, tee_box_id: int, payload: dict):
        if not payload.get('holes'):
            response_body = {
                'status': 'fail',
                'message': "RequestBody is missing required parameter: 'holes'"
            }
            return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

        holes_data = []
        for hole in payload.get('holes'):
            hole['golf_course_id'] = golf_course_id
            hole['tee_box_id'] = tee_box_id
            try:
                hole_data = self._hole_schema.load(hole).data
                holes_data.append(hole_data)
            except ValidationError as e:
                response_body = {
                    'status': 'fail',
                    'message': e.messages
                }
                return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        self._hole_repo.bulk_create(records=holes_data)
        message = "Hole records were successfully added for " \
                  f"GolfCourse id: {golf_course_id} and TeeBox id: {tee_box_id}"
        response_body = {
            'status': 'success',
            'message': message,
            'uri': f'/golf-courses/{golf_course_id}/tee-boxes/{tee_box_id}/holes/',
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)
