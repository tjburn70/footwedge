from http import HTTPStatus
from typing import List

from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.services.hole_service import HoleService
from api.repositories.golf_round_stats_repository import GolfRoundStatsRepository
from api.schemas import GolfRoundStatsSchema
from api.models import GolfRound, GolfRoundStats


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

        new_stats = self._golf_round_stats_repo.bulk_create(records=round_stats)
        results = self._golf_round_stats_schema.dump(new_stats, many=True)
        message = f"GolfRoundStats records were successfully added for GolfRound id: '{golf_round_id}'"
        response_body = {
            'status': 'success',
            'message': message,
            'uri': f'/golf-rounds/{golf_round_id}/golf-round-stats',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    @staticmethod
    def calculate_stats_summary(stats: List[GolfRoundStats], hole_ids_to_par: dict) -> dict:
        total_putts = 0
        total_fairways = 0
        total_greens_in_regulation = 0
        up_and_downs = 0
        sand_saves = 0
        for stat in stats:
            total_putts += stat.putts
            if stat.fairway_hit:
                total_fairways += 1
            if stat.green_in_regulation:
                total_greens_in_regulation += 1
            par = hole_ids_to_par.get(stat.hole_id)
            if stat.gross_score == par:
                if stat.putts == 1 and stat.chips == 1:
                    up_and_downs += 1
                if stat.putts == 1 and stat.greenside_sand_shots == 1:
                    sand_saves += 1
        stats_summary = {
            'putts': total_putts,
            'fairways': total_fairways,
            'greens_in_regulation': total_greens_in_regulation,
            'up_and_downs': up_and_downs,
            'sand_saves': sand_saves,
        }
        return stats_summary

    def stats_summary_by_round_id(self, golf_rounds: List[GolfRound], hole_service: HoleService) -> Response:
        data = {}
        for golf_round in golf_rounds:
            hole_ids = [stat.hole_id for stat in golf_round.stats]
            hole_ids_to_par = hole_service.map_hole_ids_to_par(hole_ids=hole_ids)
            # TODO: this is a hack, num_holes should be a property of golf_round
            if len(golf_round.stats) == 18:
                stats_summary = self.calculate_stats_summary(
                    stats=golf_round.stats,
                    hole_ids_to_par=hole_ids_to_par,
                )
                data[golf_round.id] = stats_summary

        response_body = {
            'status': 'success',
            'uri': f'/golf-round-stats/summary',
            'result': data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)
