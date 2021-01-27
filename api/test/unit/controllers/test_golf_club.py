import json
from datetime import datetime

from unittest.mock import patch
from http import HTTPStatus

from api.schemas import (
    GolfClubSchema,
    GolfCourseSchema,
)
from api.models import GolfCourse

GOLF_CLUB_REPO_IMPORT_PATH = "api.controllers.golf_club.golf_club_repo"
GOLF_COURSE_REPO_IMPORT_PATH = "api.controllers.golf_club.golf_course_repo"
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
            f"If no Content-Type header in POST call, expect to receive a status_code: {HTTPStatus.BAD_REQUEST}"

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

    @patch(GOLF_COURSE_REPO_IMPORT_PATH)
    def test_get_golf_courses_by_golf_club(
            self,
            mock_golf_course_repo,
            golf_club_id,
            golf_course_model,
            client,
    ):
        mock_golf_course_repo.get_by_golf_club_id.return_value = [golf_course_model]
        path = f"/api/golf-clubs/{golf_club_id}/golf-courses"
        resp = client.get(path)

        assert resp.status_code == HTTPStatus.OK, \
            f"GET /golf_clubs failed with status_code= {resp.status_code}, " \
            f"expected to receive a status_code: {HTTPStatus.OK}"
        assert len(resp.json['result']) == 1, "Expecting there to be 1 golf course returned"
        assert mock_golf_course_repo.get_by_golf_club_id.called, \
            "Expecting golf_course_repo.get_by_golf_club_id to be called"
        mock_golf_course_repo.get_by_golf_club_id.assert_called_with(
            golf_club_id=golf_club_id,
        )

    @patch(GOLF_COURSE_REPO_IMPORT_PATH)
    def test_get_golf_courses_by_golf_club_multiple_courses(
            self,
            mock_golf_course_repo,
            olympia_fields_golf_club_id,
            olympia_fields_north_course,
            olympia_fields_south_course,
            client,
    ):
        mock_golf_course_repo.get_by_golf_club_id.return_value = [
            olympia_fields_north_course,
            olympia_fields_south_course,
        ]
        path = f"/api/golf-clubs/{olympia_fields_golf_club_id}/golf-courses"
        resp = client.get(path)

        assert resp.status_code == HTTPStatus.OK, \
            f"GET /golf_clubs failed with status_code= {resp.status_code}, " \
            f"expected to receive a status_code: {HTTPStatus.OK}"
        assert len(resp.json['result']) == 2, "Expecting there to be 1 golf course returned"
        assert mock_golf_course_repo.get_by_golf_club_id.called, \
            "Expecting golf_course_repo.get_by_golf_club_id to be called"
        mock_golf_course_repo.get_by_golf_club_id.assert_called_with(
            golf_club_id=olympia_fields_golf_club_id,
        )

    @patch(f"{SEARCH_SERVICE_IMPORT_PATH}.add_golf_course")
    @patch(GOLF_COURSE_REPO_IMPORT_PATH)
    def test_add_golf_course(
            self,
            mock_golf_course_repo,
            mock_add_golf_course,
            golf_club_id,
            golf_course_post_body,
            client,
            content_type_header,
    ):
        golf_course_model = GolfCourse(
            id=-1,
            golf_club_id=golf_club_id,
            created_ts=datetime.now(),
        )
        mock_golf_course_repo.create.return_value = golf_course_model
        path = f"/api/golf-clubs/{golf_club_id}/golf-courses"
        payload = json.dumps(golf_course_post_body, default=str)
        resp = client.post(path, headers=content_type_header, data=payload)

        assert resp.status_code == HTTPStatus.OK, \
            f"POST {path} failed with status_code = {resp.status_code}, " \
            f"expected to receive a status_code: {HTTPStatus.OK}"
        assert mock_golf_course_repo.create.called, "Expecting golf_club_repo.get to be called"
        expected_payload = golf_course_post_body.copy()
        expected_payload['golf_club_id'] = golf_club_id
        mock_golf_course_repo.create.assert_called_with(data=expected_payload)
        assert mock_add_golf_course.called, "Expecting SearchService.add_golf_course to be called"

        golf_course = GolfCourseSchema().dump(golf_course_model)
        mock_add_golf_course.assert_called_with(
            golf_club_id=golf_club_id,
            payload=golf_course,
        )

    def test_add_golf_course_no_content_header(
            self,
            client,
            golf_club_id,
    ):
        path = f"/api/golf-clubs/{golf_club_id}/golf-courses"
        resp = client.post(path, headers=None, data={})
        assert resp.status_code == HTTPStatus.BAD_REQUEST, \
            f"If no Content-Type header in POST call, expect to receive a status_code: {HTTPStatus.BAD_REQUEST}"

    def test_add_golf_course_invalid_body(
            self,
            client,
            content_type_header,
    ):
        payload = json.dumps({"random_key": "I need more fields!"}, default=str)
        path = f"/api/golf-clubs/"
        resp = client.post(path, headers=content_type_header, data=payload)
        assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, \
            f"If payload is missing required fields, " \
            f"expected to receive a status_code: {HTTPStatus.UNPROCESSABLE_ENTITY}"
