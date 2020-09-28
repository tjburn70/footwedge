from http import HTTPStatus
from datetime import datetime

from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.repositories.handicap_repository import HandicapRepository
from api.schemas import HandicapSchema


class HandicapService:

    def __init__(self, repo: HandicapRepository, schema: HandicapSchema):
        self._handicap_repo = repo
        self._handicap_schema = schema

    def get_by_date(self, user_id: int, date: datetime) -> Response:
        handicaps = self._handicap_repo.get_by_date(user_id=user_id, start_date=date)
        results = self._handicap_schema.dump(handicaps, many=True)
        response_body = {
            'status': 'success',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_active(self, user_id: int) -> Response:
        current_handicap = self._handicap_repo.get_active(user_id=user_id)
        result = self._handicap_schema.dump(current_handicap)
        response_body = {
            'status': 'success',
            'result': result.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def _close_active(self, user_id: int):
        current_handicap = self._handicap_repo.get_active(user_id=user_id)
        self._handicap_repo.close(current_handicap)

    def add(self, user_id: int, payload: dict) -> Response:
        self._close_active(user_id=user_id)
        payload['user_id'] = user_id
        try:
            handicap_data = self._handicap_schema.load(payload).data
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        self._handicap_repo.create(data=handicap_data)
        response_body = {
            'status': 'success',
            'message': f"Handicap was successfully added for user_id: '{user_id}'",
            'uri': f'/handicaps',
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)
