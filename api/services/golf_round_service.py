import json
from http import HTTPStatus

import boto3
from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.repositories.golf_round_repository import GolfRoundRepository
from api.schemas import GolfRoundSchema
from api.settings import settings


sqs_client = boto3.client('sqs')


class GolfRoundService:

    def __init__(self, repo: GolfRoundRepository, schema: GolfRoundSchema):
        self._golf_round_repo = repo
        self._golf_round_schema = schema

    def get(self, _id: int) -> Response:
        golf_round = self._golf_round_repo.get(_id)
        result = self._golf_round_schema.dump(golf_round)
        response_body = {
            'status': 'success',
            'result': result.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_by_user_id(self, user_id: int) -> Response:
        rounds = self._golf_round_repo.get_by_user_id(user_id=user_id)
        results = self._golf_round_schema.dump(rounds, many=True)
        response_body = {
            'status': 'success',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def add(self, user_id: int, payload: dict) -> Response:
        payload['user_id'] = user_id
        try:
            golf_round_data = self._golf_round_schema.load(payload).data
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        new_round = self._golf_round_repo.create(data=golf_round_data)
        self._queue_handicap_calculation(user_id=user_id)

        golf_round_id = new_round.id
        result = self._golf_round_schema.dump(new_round)
        response_body = {
            'status': 'success',
            'message': f"GolfRound: '{golf_round_id}' was successfully added for user_id: '{user_id}'",
            'result': result.data,
            'uri': f'/golf-rounds/{golf_round_id}',
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    @staticmethod
    def _queue_handicap_calculation(user_id: int):
        payload = json.dumps({"user_id": user_id}, default=str)
        sqs_client.send_message(
            QueueUrl=settings.HANDICAP_QUEUE_URL,
            MessageBody=payload,
        )
