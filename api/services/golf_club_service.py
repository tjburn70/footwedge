from http import HTTPStatus

from flask import (
    Response,
    make_response,
    jsonify,
)
from marshmallow import ValidationError

from api.repositories.golf_club_repository import GolfClubRepository
from api.schemas import GolfClubSchema
from api.services.search_service import SearchService


class GolfClubService:

    def __init__(self, repo: GolfClubRepository, schema: GolfClubSchema):
        self._golf_club_repo = repo
        self._golf_club_schema = schema

    def get(self, _id: int) -> Response:
        golf_club = self._golf_club_repo.get(_id)
        result = self._golf_club_schema.dump(golf_club)
        response_body = {
            'status': 'success',
            'result': result.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def get_all(self) -> Response:
        clubs = self._golf_club_repo.get_all()
        results = self._golf_club_schema.dump(clubs, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    def add(self, payload: dict) -> Response:
        try:
            golf_club_data = self._golf_club_schema.load(payload).data
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        golf_club_model = self._golf_club_repo.create(data=golf_club_data)
        golf_club = self._golf_club_schema.dump(golf_club_model).data
        # TODO: Is this the best way, maybe make an async future
        SearchService.add_golf_club(
            golf_club_id=golf_club.id,
            payload=golf_club,
        )
        response_body = {
            'status': 'success',
            'message': f"Golf Club: '{golf_club_model.name}' was successfully added",
            'd': golf_club,
            'uri': f'api/golf-clubs/{golf_club_model.id}',
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)
