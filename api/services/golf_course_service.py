from http import HTTPStatus
from typing import List

from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.repositories.golf_course_repository import GolfCourseRepository
from api.schemas import GolfCourseSchema
from api.services.search_service import SearchService


class GolfCourseService:

    def __init__(self, repo: GolfCourseRepository, schema: GolfCourseSchema):
        self._golf_course_repo = repo
        self._golf_course_schema = schema

    def get(self, _id: int) -> Response:
        golf_course = self._golf_course_repo.get(_id)
        result = self._golf_course_schema.dump(golf_course)
        response_body = {
            'status': 'success',
            'result': result.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_by_ids(self, ids: List[int]) -> Response:
        golf_courses = self._golf_course_repo.get_by_ids(ids=ids)
        results = self._golf_course_schema.dump(golf_courses, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_all(self) -> Response:
        courses = self._golf_course_repo.get_all()
        results = self._golf_course_schema.dump(courses, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_by_golf_club_id(self, golf_club_id: int):
        courses = self._golf_course_repo.get_by_golf_club_id(golf_club_id=golf_club_id)
        results = self._golf_course_schema.dump(courses, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def add(self, payload: dict) -> Response:
        try:
            golf_course_data = self._golf_course_schema.load(payload).data
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        golf_course_model = self._golf_course_repo.create(data=golf_course_data)
        golf_course = self._golf_course_schema.dump(golf_course_model).data
        golf_club_id = golf_course_model.golf_club_id
        # TODO: Is this the best way, maybe make an async future
        SearchService.add_golf_course(
            golf_club_id=golf_club_id,
            payload=golf_course
        )
        response_body = {
            'status': 'success',
            'message': f"Golf Course: '{golf_course_model.name}' was successfully added",
            'result': golf_course,
            'uri': f'api/golf-courses/{golf_course_model.id}',
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def delete(self, _id: int):
        is_deleted = self._golf_course_repo.delete(model_id=_id)
        if not is_deleted:
            response_body = {
                'status': 'fail',
                'message': f'No Golf Course with id: {_id}',
            }
            return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

        return make_response("", HTTPStatus.NO_CONTENT.value)
