from unittest.mock import MagicMock
from datetime import datetime

import pytest

from api.index import app
from api.services.golf_club_service import GolfClubService
from api.models import GolfClub
from api.schemas import GolfClubSchema


@pytest.fixture
def golf_club_model():
    return GolfClub(
        id=1,
        name="Test Golf Club",
        address="124 Pleasant Lane",
        city="Chicago",
        state_code="IL",
        county="DuPage",
        zip_code="60515",
        phone_number="630-555-8899",
        email="fairways_and_greens@gmail.com",
        created_ts=datetime.utcnow(),
        touched_ts=None,
        golf_courses=[],
    )


def test_get(golf_club_model):
    with app.app_context():
        mock_repo = MagicMock()
        mock_repo.get.return_value = golf_club_model
        golf_club_service = GolfClubService(
            repo=mock_repo,
            schema=GolfClubSchema(),
        )

        resp = golf_club_service.get(_id=1)

        expected_status_code = 200
        assert expected_status_code == resp.status_code
