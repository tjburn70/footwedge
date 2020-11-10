import random
import json
import uuid
from decimal import Decimal
from datetime import datetime

import pytest

from lib.models import GolfRound, TeeBox
from lib.footwedge_api import FootwedgeApi


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration"
    )


@pytest.fixture(scope="class")
def footwedge_api_client():
    return FootwedgeApi()


@pytest.fixture(scope="class")
def golf_club(footwedge_api_client: FootwedgeApi):
    request_body = {
        "name": "Test Golf Club",
        "address": "18 Fairways and Greens Avenue",
        "city": "Chicago",
        "state_code": "IL",
        "county": "Cook County",
        "zip_code": "60647",
        "phone_number": "(312) 555-1234",
        "email": ""
    }

    method = "post"
    path = "/golf-clubs"
    headers = {"Content-Type": "application/json"}
    resp = footwedge_api_client.call(
        method=method,
        path=path,
        headers=headers,
        data=json.dumps(request_body, default=str)
    )
    resp.raise_for_status()
    result = resp.json()['result']
    yield result

    print("Cleaning up golf_club_factory...")
    # golf_club_id = result.get('id')
    # delete_path = f"{path}/{golf_club_id}"
    # footwedge_api_client.call(
    #     method="delete",
    #     path=delete_path,
    # )


@pytest.fixture(scope="class")
def golf_course_factory(footwedge_api_client: FootwedgeApi):
    golf_club_id_to_golf_course_id = {}

    def _golf_course_factory(golf_club_id: int):
        request_body = {
            "name": "Test Golf Course",
            "num_holes": 18,
        }
        method = "post"
        path = f"/golf-clubs/{golf_club_id}/golf-courses"
        headers = {"Content-Type": "application/json"}
        resp = footwedge_api_client.call(
            method=method,
            path=path,
            headers=headers,
            data=json.dumps(request_body, default=str)
        )
        resp.raise_for_status()
        result = resp.json()['result']
        golf_course_id = result.get('id')
        golf_club_id_to_golf_course_id[golf_course_id] = golf_club_id
        return result

    yield _golf_course_factory

    print("Cleaning up golf_course_factory...")
    # for club_id, course_id in golf_club_id_to_golf_course_id.items():
    #     delete_path = f"api/golf-clubs/{club_id}/golf-courses/{course_id}"
    #     footwedge_api_client.call(
    #         method="delete",
    #         path=delete_path,
    #     )


@pytest.fixture(scope="class")
def tee_box_factory(footwedge_api_client: FootwedgeApi):
    golf_course_id_to_tee_box_id = {}

    def _tee_box_factory(golf_course_id: int, par: int, course_rating: Decimal, slope: Decimal):
        request_body = {
            "tee_color": "Blue",
            "par": par,
            "distance": "6305",
            "unit": "yards",
            "course_rating": course_rating,
            "slope": slope,
        }
        method = "post"
        path = f"/golf-courses/{golf_course_id}/tee-boxes"
        headers = {"Content-Type": "application/json"}
        resp = footwedge_api_client.call(
            method=method,
            path=path,
            headers=headers,
            data=json.dumps(request_body, default=str)
        )
        resp.raise_for_status()
        result = resp.json()['result']
        tee_box_id = result.get('id')
        golf_course_id_to_tee_box_id[golf_course_id] = tee_box_id
        return result

    yield _tee_box_factory

    print("Cleaning up tee_box_factory...")
    # for club_id, course_id in golf_course_id_to_tee_box_id.items():
    #     delete_path = f"api/golf-clubs/{club_id}/golf-courses/{course_id}"
    #     footwedge_api_client.call(
    #         method="delete",
    #         path=delete_path,
    #     )


@pytest.fixture(scope="class")
def user(footwedge_api_client: FootwedgeApi):
    unique_identifier = str(uuid.uuid4())
    request_body = {
        "email": f"test-user-{unique_identifier}@gmail.com",
        "password": "test",
        "first_name": "test",
        "last_name": f"test-user-{unique_identifier}"
    }
    method = "post"
    path = "/user/register"
    headers = {"Content-Type": "application/json"}
    resp = footwedge_api_client.call(
        method=method,
        path=path,
        headers=headers,
        data=json.dumps(request_body, default=str)
    )
    resp.raise_for_status()
    resp_body = resp.json()
    yield resp_body

    print("Cleaning up user...")
    # user_id = resp_body.get('user_id')
    # delete_path = f"api/user/{user_id}"
    # footwedge_api_client.call(
    #     method="delete",
    #     path=delete_path,
    # )


@pytest.fixture
def tee_box_model():
    tee_box_id = random.randrange(1, 1000, 1)
    golf_course_id = random.randrange(1, 1000, 1)
    tee_color = "Blue"
    par = random.randrange(70, 73, 1)
    distance = random.randrange(6000, 7550, 20)
    unit = "yards"
    course_rating = 73.1
    slope = 133.0
    return TeeBox(
        id=tee_box_id,
        golf_course_id=golf_course_id,
        tee_color=tee_color,
        par=par,
        distance=distance,
        unit=unit,
        course_rating=course_rating,
        slope=slope,
    )


@pytest.fixture
def golf_round_model_factory():
    def _golf_round_model_factory(user_id: int, tee_box_id: int):
        golf_round_id = random.randrange(1, 1000, 1)
        golf_course_id = random.randrange(1, 1000, 1)
        gross_score = random.randrange(65, 120, 1)
        towards_handicap = random.choice([True, False])
        played_on = datetime.now().strftime('%Y-%m-%d')
        return GolfRound(
            id=golf_round_id,
            golf_course_id=golf_course_id,
            tee_box_id=tee_box_id,
            user_id=user_id,
            gross_score=gross_score,
            towards_handicap=towards_handicap,
            played_on=played_on,
        )
    return _golf_round_model_factory


