from datetime import datetime

import pytest

from api.index import create_app
from api.models import (
    Hole,
    TeeBox,
    GolfCourse,
    GolfClub,
)


class TestAppConfig:
    TESTING = True
    APP_NAME = "test-footwedge"


@pytest.fixture
def app():
    app = create_app(TestAppConfig)
    yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def content_type_header():
    return {"Content-Type": "application/json"}


@pytest.fixture
def tee_box_id():
    return 1


@pytest.fixture
def golf_course_id():
    return 1


@pytest.fixture
def golf_club_id():
    return 1


@pytest.fixture
def blue_tee_box(tee_box_id, golf_course_id):
    return TeeBox(
        id=tee_box_id,
        golf_course_id=golf_course_id,
        tee_color="Blue",
        par=72,
        distance=7150,
        unit="yards",
        course_rating=135.8,
        slope=144.0,
        created_ts=datetime.now(),
        touched_ts=None,
        golf_holes=[],
    )


@pytest.fixture
def golf_course(golf_course_id, golf_club_id, blue_tee_box):
    return GolfCourse(
        id=golf_course_id,
        golf_club_id=golf_club_id,
        name="Champions - Main",
        num_holes=18,
        created_ts=datetime.now(),
        touched_ts=None,
        tee_boxes=[blue_tee_box]
    )


@pytest.fixture
def random_golf_club_model_with_golf_course(golf_club_id, golf_course):
    return GolfClub(
        id=golf_club_id,
        name="Prestigious Golf Club",
        address="123 Fairways and Greens",
        city="Houston",
        state_code="TX",
        zip_code="77024",
        phone_number="713-555-1234",
        email="champions_club@gmail.com",
        created_ts=datetime.now(),
        touched_ts=None,
        golf_courses=[golf_course],
    )


@pytest.fixture
def golf_club_dict():
    return dict(
        name="Some Golf Club",
        address="123 Fairways and Greens",
        city="Chicago",
        state_code="IL",
        zip_code="60647",
        phone_number="312-555-1234",
        email="great_club@gmail.com",
    )


@pytest.fixture
def golf_club_model_no_golf_course(golf_club_dict):
    return GolfClub(id=-1, **golf_club_dict)
