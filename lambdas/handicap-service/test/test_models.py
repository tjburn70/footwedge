from datetime import datetime

import pytest
from pydantic.error_wrappers import ValidationError

from lib.models import (
    GolfRound,
    TeeBox
)


@pytest.fixture
def golf_round_data():
    payload = {
        'id': 1,
        'golf_course_id': 1,
        'tee_box_id': 1,
        'user_id': 1,
        'gross_score': 70,
        'towards_handicap': True,
        'played_on': '2020-01-01',
    }
    return payload


@pytest.fixture
def tee_box_data():
    payload = {
        'id': 1,
        'golf_course_id': 1,
        'tee_color': "Blue",
        'par': 72,
        'distance': 6950,
        'unit': "yards",
        'course_rating': 73.7,
        'slope': 137.0,
    }
    return payload


def test_golf_round_model(golf_round_data):
    GolfRound(**golf_round_data)
    GolfRound(
        id=1,
        golf_course_id="2",
        tee_box_id=3,
        user_id=4,
        gross_score=100.123,
        towards_handicap="false",
        played_on=datetime.now()
    )


def test_golf_round_model_invalid_types():
    with pytest.raises(ValidationError):
        GolfRound(
            id="not-an-int",
            golf_course_id=1,
            tee_box_id=2,
            user_id=3,
            gross_score=4,
            towards_handicap=True,
            played_on=datetime.now()

        )


def test_golf_round_model_missing_required_keys():
    with pytest.raises(ValidationError):
        GolfRound(
            id=1
        )


def test_tee_box_model(tee_box_data):
    TeeBox(**tee_box_data)


def test_tee_box_model_invalid_types():
    with pytest.raises(ValidationError):
        TeeBox(
            id=1,
            golf_course_id=1,
            tee_color="black",
            par=72,
            distance=7000,
            unit="yards",
            course_rating="not-decimal",
            slope="130",
        )


def test_tee_box_model_missing_required_keys(tee_box_data):
    with pytest.raises(ValidationError):
        TeeBox()
