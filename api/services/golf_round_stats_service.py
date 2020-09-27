from http import HTTPStatus

from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.repositories.golf_round_stats_repository import GolfRoundStatsRepository
from api.schemas import GolfRoundStatsSchema


class GolfRoundStatsService:

    def __init__(self, repo: GolfRoundStatsRepository, schema: GolfRoundStatsSchema):
        self._golf_round_stats_repo = repo
        self._golf_round_stats_schema = schema

    def get_by_golf_round_id(self, golf_round_id: int) -> Response:
        rounds = self._golf_round_stats_repo.get_by_golf_round_id(golf_round_id=golf_round_id)
        results = self._golf_round_stats_schema.dump(rounds, many=True)
        response_body = {
            'status': 'success',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def add(self, golf_round_id: int, payload: dict) -> Response:
        if not payload.get('round_stats'):
            response_body = {
                'status': 'fail',
                'message': "Request is missing required parameter: 'round_stats'"
            }
            return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

        round_stats = []
        for hole_stat in payload['round_stats']:
            hole_stat['golf_round_id'] = golf_round_id
            try:
                round_stat_data = self._golf_round_stats_schema.load(hole_stat).data
            except ValidationError as e:
                response_body = {
                    'status': 'fail',
                    'message': e.messages
                }
                return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)
            round_stats.append(round_stat_data)

        self._golf_round_stats_repo.bulk_create(records=round_stats)
        results = self._golf_round_stats_schema.dump(round_stats, many=True)
        message = f"GolfRoundStats records were successfully added for GolfRound id: '{golf_round_id}'"
        response_body = {
            'status': 'success',
            'message': message,
            'uri': f'/golf-rounds/{golf_round_id}/golf-round-stats',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)
