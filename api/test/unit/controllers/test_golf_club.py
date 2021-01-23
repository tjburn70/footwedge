import json

from unittest.mock import patch
from http import HTTPStatus

from api.schemas import GolfClubSchema

GOLF_CLUB_REPO_IMPORT_PATH = "api.controllers.golf_club.golf_club_repo"
SEARCH_SERVICE_IMPORT_PATH = "api.controllers.golf_club.golf_club_service.SearchService"


class TestGolfClub:

    @patch(GOLF_CLUB_REPO_IMPORT_PATH)
    def test_get_golf_clubs(
            self,
            mock_golf_club_repo,
            client,
            random_golf_club_model_with_golf_course,
            golf_club_model_no_golf_course,
    ):
        mock_golf_club_repo.get_all.return_value = [
            random_golf_club_model_with_golf_course,
            golf_club_model_no_golf_course
        ]

        resp = client.get("/api/golf-clubs/")

        assert resp.status_code == HTTPStatus.OK, \
            f"GET /golf_clubs failed with status_code= {resp.status_code}, " \
            f"expected to receive a status_code: {HTTPStatus.OK}"
        assert len(resp.json['result']) == 2, "Expecting there to be 2 golf clubs returned"
        assert mock_golf_club_repo.get_all.called, "Expecting golf_club_repo.get_all to be called"

    @patch(GOLF_CLUB_REPO_IMPORT_PATH)
    def test_get_golf_clubs_by_id(
            self,
            mock_golf_club_repo,
            client,
            golf_club_id,
            random_golf_club_model_with_golf_course,
    ):
        mock_golf_club_repo.get.return_value = random_golf_club_model_with_golf_course
        path = f"/api/golf-clubs/{golf_club_id}"
        resp = client.get(path)

        assert resp.status_code == HTTPStatus.OK, \
            f"GET {path} failed with status_code = {resp.status_code}, " \
            f"expected to receive a status_code: {HTTPStatus.OK}"
        assert mock_golf_club_repo.get.called, "Expecting golf_club_repo.get to be called"
        mock_golf_club_repo.get.assert_called_with(golf_club_id)

    @patch(f"{SEARCH_SERVICE_IMPORT_PATH}.add_golf_club")
    @patch(GOLF_CLUB_REPO_IMPORT_PATH)
    def test_add_golf_club(
            self,
            mock_golf_club_repo,
            mock_add_golf_club,
            client,
            content_type_header,
            golf_club_dict,
            golf_club_model_no_golf_course,
    ):
        mock_golf_club_repo.create.return_value = golf_club_model_no_golf_course
        path = "/api/golf-clubs/"
        payload = json.dumps(golf_club_dict, default=str)
        resp = client.post(path, headers=content_type_header, data=payload)

        assert resp.status_code == HTTPStatus.OK, \
            f"POST {path} failed with status_code = {resp.status_code}, " \
            f"expected to receive a status_code: {HTTPStatus.OK}"
        assert mock_golf_club_repo.create.called, "Expecting golf_club_repo.get to be called"
        mock_golf_club_repo.create.assert_called_with(data=golf_club_dict)
        assert mock_add_golf_club.called, "Expecting SearchService.add_golf_club to be called"

        golf_club_id = golf_club_model_no_golf_course.id
        golf_club = GolfClubSchema().dump(golf_club_model_no_golf_course)
        mock_add_golf_club.assert_called_with(
            golf_club_id=golf_club_id,
            payload=golf_club,
        )

    def test_add_golf_club_no_content_header(
            self,
            client,
    ):
        path = "/api/golf-clubs/"
        resp = client.post(path, headers=None, data={})
        assert resp.status_code == HTTPStatus.BAD_REQUEST, \
            f"If no Content-Type header in POST call, expect to receive a status_code: {HTTPStatus.OK}"

    def test_add_golf_club_invalid_body(
            self,
            client,
            content_type_header,
    ):
        payload = {"random_key": "I need more fields!"}
        path = f"/api/golf-clubs/"
        resp = client.post(path, json=payload)
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, \
            f"If payload is missing required fields, " \
            f"expected to receive a status_code: {HTTPStatus.UNPROCESSABLE_ENTITY}"
