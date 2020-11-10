import random
from decimal import Decimal
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from lib.service import HandicapService
from lib.footwedge_api import FootwedgeApi
from lib.models import (
    GolfRound,
    TeeBox,
)
from lib.exceptions import (
    HandicapServiceFailure,
    SampleSizeTooSmall,
)


@pytest.fixture
def sorted_score_differentials():
    return [
        Decimal('1.123'),
        Decimal('2.2345'),
        Decimal('3.345'),
        Decimal('4.4567'),
        Decimal('5.567'),
        Decimal('6.6789'),
        Decimal('7.789'),
        Decimal('8.8901'),
        Decimal('9.912'),
        Decimal('10.2345'),
        Decimal('11.345'),
        Decimal('12.45670'),
        Decimal('13.567'),
        Decimal('14.6789'),
        Decimal('15.7890'),
        Decimal('16.890'),
        Decimal('17.1234'),
        Decimal('18.23'),
        Decimal('19.457098'),
        Decimal('20.0000123'),
    ]


@pytest.fixture
def random_differential_factory():
    def _random_differential_factory(num_differentials: int, lower_bound: int, upper_bound: int, precision: int = 100):
        differentials = []
        for x in range(num_differentials):
            differential = Decimal(random.randrange(lower_bound, upper_bound)) / precision
            differentials.append(differential)
        return differentials
    return _random_differential_factory


@pytest.fixture
def golf_round_factory():
    def _golf_round_factory(tee_box_id: int):
        golf_round_id = random.randrange(1, 1000, 1)
        golf_course_id = random.randrange(1, 1000, 1)
        user_id = random.randrange(1, 1000, 1)
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
    return _golf_round_factory


@pytest.fixture
def tee_box():
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


class TestHandicapService:

    def test_get_golf_rounds_bad_request(self):
        mock_footwedge_api_client = MagicMock()
        mock_response = MagicMock()
        mock_footwedge_api_client.call.return_value = mock_response
        mock_response.ok = False

        handicap_service = HandicapService(
            footwedge_api_client=mock_footwedge_api_client,
            user_id=1,
        )
        with pytest.raises(HandicapServiceFailure):
            handicap_service._get_golf_rounds()

    def test_get_golf_rounds(self):
        mock_footwedge_api_client = MagicMock()
        mock_response = MagicMock()
        mock_footwedge_api_client.call.return_value = mock_response
        mock_response.ok = True
        golf_round_dict = {
            'id': 1,
            'golf_course_id': 1,
            'tee_box_id': 1,
            'user_id': 1,
            'gross_score': 70,
            'towards_handicap': True,
            'played_on': datetime.now().strftime('%Y-%m-%d')
        }
        response_body = {
            "result": [golf_round_dict]
        }
        mock_response.json.return_value = response_body
        expected_golf_rounds = [GolfRound(**golf_round_dict)]

        handicap_service = HandicapService(
            footwedge_api_client=mock_footwedge_api_client,
            user_id=1,
        )
        golf_rounds = handicap_service._get_golf_rounds()

        assert expected_golf_rounds == golf_rounds

    def test_get_tee_box_bad_request(self):
        mock_footwedge_api_client = MagicMock()
        mock_response = MagicMock()
        mock_footwedge_api_client.call.return_value = mock_response
        mock_response.ok = False

        handicap_service = HandicapService(
            footwedge_api_client=mock_footwedge_api_client,
            user_id=1,
        )
        with pytest.raises(HandicapServiceFailure):
            handicap_service._get_tee_box(tee_box_id=1)

    def test_get_tee_box(self):
        mock_footwedge_api_client = MagicMock()
        mock_response = MagicMock()
        mock_footwedge_api_client.call.return_value = mock_response
        mock_response.ok = True
        tee_box_dict = {
            'id': 1,
            'golf_course_id': 1,
            'tee_color': "Blue",
            'par': 72,
            'distance': 6500,
            'unit': "yards",
            'course_rating': '72.6',
            'slope': '127',
        }
        response_body = {
            "result": tee_box_dict
        }
        mock_response.json.return_value = response_body
        expected_tee_box = TeeBox(**tee_box_dict)

        handicap_service = HandicapService(
            footwedge_api_client=mock_footwedge_api_client,
            user_id=1,
        )
        tee_box = handicap_service._get_tee_box(tee_box_id=1)

        assert expected_tee_box == tee_box

    def test_calculate_differential(self):
        gross_score = 79
        course_rating = Decimal('73.1')
        slope = Decimal('138')

        expected_differential = Decimal('4.831159420289855072463768116')
        differential = HandicapService.calculate_differential(
            gross_score=gross_score,
            course_rating=course_rating,
            slope=slope,
        )
        print(type(differential))
        assert expected_differential == differential, f"Expected the differential to be: {expected_differential}"

    def test_determine_sample_size_too_small(self):
        num_rounds = 4
        with pytest.raises(SampleSizeTooSmall):
            HandicapService.determine_sample_size(num_rounds=num_rounds)

    def test_determine_sample_size_10_rounds(self):
        expected_sample_size = 1
        num_rounds_min_bound = 5
        actual_sample_size = HandicapService.determine_sample_size(
            num_rounds=num_rounds_min_bound
        )
        assert expected_sample_size == actual_sample_size, \
            f"For num_rounds = '{num_rounds_min_bound}' expected the sample_size to be: '{expected_sample_size}'"

        num_rounds_max_bound = 10
        actual_sample_size = HandicapService.determine_sample_size(
            num_rounds=num_rounds_max_bound
        )
        assert expected_sample_size == actual_sample_size, \
            f"For num_rounds = '{num_rounds_max_bound}' expected the sample_size to be: '{expected_sample_size}'"

    def test_determine_sample_size_between_10_and_20_rounds(self):
        expected_sample_size = 5
        num_rounds_min_bound = 11
        actual_sample_size = HandicapService.determine_sample_size(
            num_rounds=num_rounds_min_bound
        )
        assert expected_sample_size == actual_sample_size, \
            f"For num_rounds = '{num_rounds_min_bound}' expected the sample_size to be: '{expected_sample_size}'"

        num_rounds_max_bound = 19
        actual_sample_size = HandicapService.determine_sample_size(
            num_rounds=num_rounds_max_bound
        )
        assert expected_sample_size == actual_sample_size, \
            f"For num_rounds = '{num_rounds_max_bound}' expected the sample_size to be: '{expected_sample_size}'"

    def test_determine_sample_size_20_rounds(self):
        expected_sample_size = 10
        num_rounds_min_bound = 20
        actual_sample_size = HandicapService.determine_sample_size(
            num_rounds=num_rounds_min_bound
        )
        assert expected_sample_size == actual_sample_size, \
            f"For num_rounds = '{num_rounds_min_bound}' expected the sample_size to be: '{expected_sample_size}'"

    def test_determine_lowest_differential_sample_size_too_small(self):
        differentials = [Decimal(1.1), Decimal(2.2), Decimal(3.3)]
        handicap_service = HandicapService(
            footwedge_api_client=FootwedgeApi(),
            user_id=1,
        )
        with pytest.raises(SampleSizeTooSmall):
            handicap_service.determine_lowest_differential(differentials=differentials)

    def test_determine_lowest_differential_sample_size_too_large(self, random_differential_factory):
        handicap_service = HandicapService(
            footwedge_api_client=FootwedgeApi(),
            user_id=1,
        )
        mock_determine_sample_size = MagicMock()
        mock_determine_sample_size.side_effect = HandicapServiceFailure()
        handicap_service.determine_sample_size = mock_determine_sample_size
        differentials = random_differential_factory(
            num_differentials=10,
            lower_bound=150,
            upper_bound=300,
            precision=100,
        )
        with pytest.raises(HandicapServiceFailure):
            handicap_service.determine_lowest_differential(differentials=differentials)

    def test_determine_lowest_differential_between_5_and_10_rounds(self, random_differential_factory):
        num_differentials = 6
        differentials = random_differential_factory(
            num_differentials=num_differentials,
            lower_bound=150,
            upper_bound=300,
            precision=100,
        )
        expected_sample_size = 1
        expected_differentials = sorted(differentials)[:expected_sample_size]

        handicap_service = HandicapService(
            footwedge_api_client=FootwedgeApi(),
            user_id=1,
        )
        actual_differentials = handicap_service.determine_lowest_differential(differentials=differentials)

        assert expected_differentials == actual_differentials, "The lowest differential should be returned"

    def test_determine_lowest_differential_between_10_and_20_rounds(self, random_differential_factory):
        num_differentials = 15
        differentials = random_differential_factory(
            num_differentials=num_differentials,
            lower_bound=100,
            upper_bound=600,
            precision=100,
        )
        expected_sample_size = 5
        expected_differentials = sorted(differentials)[:expected_sample_size]

        handicap_service = HandicapService(
            footwedge_api_client=FootwedgeApi(),
            user_id=1,
        )
        actual_differentials = handicap_service.determine_lowest_differential(differentials=differentials)

        assert expected_differentials == actual_differentials, \
            f"The {expected_sample_size} lowest differentials should be returned"

    def test_determine_lowest_differential_20_rounds(self, random_differential_factory):
        num_differentials = 30
        differentials = random_differential_factory(
            num_differentials=num_differentials,
            lower_bound=100,
            upper_bound=600,
            precision=100,
        )
        expected_sample_size = 10
        expected_differentials = sorted(differentials)[:expected_sample_size]

        handicap_service = HandicapService(
            footwedge_api_client=FootwedgeApi(),
            user_id=1,
        )
        actual_differentials = handicap_service.determine_lowest_differential(differentials=differentials)

        assert expected_differentials == actual_differentials, \
            f"The {expected_sample_size} lowest differentials should be returned"

    def test_calculate_handicap_index(self, sorted_score_differentials):
        handicap_service = HandicapService(
            footwedge_api_client=FootwedgeApi(),
            user_id=1,
        )
        expected_handicap_index = Decimal('5.8')
        handicap_index = handicap_service.calculate_handicap_index(differentials=sorted_score_differentials)

        assert expected_handicap_index == handicap_index, \
            f"For the differentials: {sorted_score_differentials}, expect a handicap of {expected_handicap_index}"

    def test_post_handicap_not_enough_golf_rounds(self, tee_box, golf_round_factory):
        golf_round = golf_round_factory(tee_box_id=tee_box.id)
        mock_footwedge_api_client = MagicMock()
        mock_get_golf_rounds = MagicMock()
        mock_get_golf_rounds.return_value = [golf_round]
        mock_get_tee_box = MagicMock()
        mock_get_tee_box.return_value = tee_box

        handicap_service = HandicapService(
            footwedge_api_client=mock_footwedge_api_client,
            user_id=1,
        )
        handicap_service._get_golf_rounds = mock_get_golf_rounds
        handicap_service._get_tee_box = mock_get_tee_box

        handicap_service.post_handicap()

        assert not mock_footwedge_api_client.call.called, \
            "If not enough golf_rounds for a user, do not expect the footwedge_api to be called"

    def test_post_handicap(self, tee_box, golf_round_factory):
        golf_round = golf_round_factory(tee_box_id=tee_box.id)
        mock_footwedge_api_client = MagicMock()
        mock_get_golf_rounds = MagicMock()
        mock_get_golf_rounds.return_value = [golf_round, golf_round, golf_round, golf_round, golf_round]
        mock_get_tee_box = MagicMock()
        mock_get_tee_box.return_value = tee_box

        handicap_service = HandicapService(
            footwedge_api_client=mock_footwedge_api_client,
            user_id=1,
        )
        handicap_service._get_golf_rounds = mock_get_golf_rounds
        handicap_service._get_tee_box = mock_get_tee_box

        handicap_service.post_handicap()

        assert mock_footwedge_api_client.call.called, \
            "If > 5 golf_rounds for a user, we expect the footwedge_api to be called"
