import random
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from lib.service import HandicapService
from lib.footwedge_api import FootwedgeApi
from lib.exceptions import HandicapServiceFailure, SampleSizeTooSmall


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


class TestHandicapService:

    def test_get_golf_rounds_bad_request(self):
        pass

    def test_get_golf_rounds(self):
        pass

    def test_get_tee_box_bad_request(self):
        pass

    def test_get_tee_box(self):
        pass

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

    def test_calculate_handicap_index(self):
        pass

    def test_post_handicap(self):
        pass