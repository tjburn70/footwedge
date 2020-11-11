from decimal import Decimal
from unittest.mock import patch

import pytest

from lib.models import TeeBox
from lib.exceptions import (
    SampleSizeTooSmall,
    HandicapServiceFailure,
)
from lib.service import HandicapService

HANDICAP_SERVICE_IMPORT_PATH = 'lib.service.HandicapService'
IMPOSSIBLY_LARGE_INT = 10000000000000000000


@pytest.mark.integration
class TestHandicapService:

    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls, golf_club, golf_course_factory, tee_box_factory, user, footwedge_api_client):
        cls.golf_club_id = golf_club.get('id')

        cls.golf_course_data = golf_course_factory(golf_club_id=cls.golf_club_id)
        cls.golf_course_id = cls.golf_course_data.get('id')

        cls.par = 72
        cls.course_rating = Decimal(73.5)
        cls.slope = Decimal(134.0)
        cls.tee_box_data = tee_box_factory(
            golf_course_id=cls.golf_course_id,
            par=cls.par,
            course_rating=cls.course_rating,
            slope=cls.slope,
        )
        cls.tee_box_id = cls.tee_box_data.get('id')

        cls.user_id = user.get('user_id')

        cls.footwedge_api_client = footwedge_api_client
        cls.handicap_service = HandicapService(
            footwedge_api_client=footwedge_api_client,
            user_id=cls.user_id,
        )

    def test_get_golf_rounds_user_no_golf_rounds(self):
        invalid_user_id = IMPOSSIBLY_LARGE_INT
        handicap_svc = HandicapService(
            footwedge_api_client=self.footwedge_api_client,
            user_id=invalid_user_id
        )
        with pytest.raises(HandicapServiceFailure):
            handicap_svc._get_golf_rounds()

    def test_get_golf_rounds(self):
        results = self.handicap_service._get_golf_rounds()
        print(results)

    def test_get_tee_box_invalid_id(self):
        invalid_tee_box_id = IMPOSSIBLY_LARGE_INT
        with pytest.raises(HandicapServiceFailure):
            self.handicap_service._get_tee_box(
                tee_box_id=invalid_tee_box_id,
            )

    def test_get_tee_box(self):
        actual_tee_box = self.handicap_service._get_tee_box(
            tee_box_id=self.tee_box_id,
        )
        expected_tee_box = TeeBox(**self.tee_box_data)
        assert actual_tee_box == expected_tee_box, f"Expected a result = {expected_tee_box.json()}"

    @patch(f'{HANDICAP_SERVICE_IMPORT_PATH}.post_handicap')
    @patch(f'{HANDICAP_SERVICE_IMPORT_PATH}._get_golf_rounds')
    def test_post_handicap_not_enough_golf_rounds(self,
                                                  mock_get_golf_rounds,
                                                  mock_post_handicap,
                                                  golf_round_model_factory):
        user_id_not_enough_rounds = -1
        golf_round = golf_round_model_factory(
            user_id=user_id_not_enough_rounds,
            tee_box_id=self.tee_box_id,
        )
        mock_get_golf_rounds.return_value = [golf_round]
        handicap_svc = HandicapService(
            footwedge_api_client=self.footwedge_api_client,
            user_id=user_id_not_enough_rounds
        )

        handicap_svc.add_handicap()

        assert not mock_post_handicap.called
