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
        course_rating=74.1,
        slope=144.0,
        created_ts=datetime.now(),
        touched_ts=None,
        golf_holes=[],
    )


@pytest.fixture
def golf_course_model(golf_course_id, golf_club_id, blue_tee_box):
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
def random_golf_club_model_with_golf_course(golf_club_id, golf_course_model):
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
        golf_courses=[golf_course_model],
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


@pytest.fixture
def golf_course_post_body():
    return {
        'name': 'A Wonderful Course',
        'num_holes': 18,
    }


@pytest.fixture
def olympia_fields_golf_club_id():
    return 2


@pytest.fixture
def olympia_fields_north_course_id():
    return 2


@pytest.fixture
def olympia_fields_south_course_id():
    return 3


@pytest.fixture
def olympia_fields_north_black_tee_box(olympia_fields_north_course_id):
    return TeeBox(
        id=2,
        golf_course_id=olympia_fields_north_course_id,
        tee_color="Black",
        par=70,
        distance=7273,
        unit="yards",
        course_rating=76.6,
        slope=150.0,
        created_ts=datetime.now(),
        touched_ts=None,
        golf_holes=[],
    )


@pytest.fixture
def olympia_fields_south_black_tee_box(olympia_fields_south_course_id):
    return TeeBox(
        id=3,
        golf_course_id=olympia_fields_south_course_id,
        tee_color="Black",
        par=71,
        distance=7106,
        unit="yards",
        course_rating=75.0,
        slope=146.0,
        created_ts=datetime.now(),
        touched_ts=None,
        golf_holes=[],
    )


@pytest.fixture
def olympia_fields_north_course(
        olympia_fields_north_course_id,
        olympia_fields_golf_club_id,
        olympia_fields_north_black_tee_box,
):
    return GolfCourse(
        id=olympia_fields_north_course_id,
        golf_club_id=olympia_fields_golf_club_id,
        name="Olympia Fields CC - North",
        num_holes=18,
        created_ts=datetime.now(),
        touched_ts=None,
        tee_boxes=[olympia_fields_north_black_tee_box]
    )


@pytest.fixture
def olympia_fields_south_course(
        olympia_fields_south_course_id,
        olympia_fields_golf_club_id,
        olympia_fields_south_black_tee_box,
):
    return GolfCourse(
        id=olympia_fields_south_course_id,
        golf_club_id=olympia_fields_golf_club_id,
        name="Olympia Fields CC - South",
        num_holes=18,
        created_ts=datetime.now(),
        touched_ts=None,
        tee_boxes=[olympia_fields_south_black_tee_box]
    )


@pytest.fixture
def olympia_fields(
        olympia_fields_golf_club_id,
        olympia_fields_north_course,
        olympia_fields_south_course,
):
    return GolfClub(
        id=olympia_fields_golf_club_id,
        name="Olympia Fields Country Club",
        address="2800 Country Club Dr",
        city="Olympia Fields",
        state_code="IL",
        zip_code="60461",
        phone_number="708-748-0495",
        email="",
        created_ts=datetime.now(),
        touched_ts=None,
        golf_courses=[olympia_fields_north_course, olympia_fields_south_course],
    )
