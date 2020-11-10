import json
from decimal import Decimal
from typing import List

from lib.footwedge_api import FootwedgeApi
from lib.models import (
    GolfRound,
    TeeBox,
)
from lib.exceptions import (
    SampleSizeTooSmall,
    HandicapServiceFailure,
)


class HandicapService:

    def __init__(self, footwedge_api_client: FootwedgeApi, user_id: int):
        self.footwedge_api_client = footwedge_api_client
        self.user_id = user_id

    def _get_golf_rounds(self) -> List[GolfRound]:
        path = f"/golf-rounds/{self.user_id}"
        resp = self.footwedge_api_client.call(method="get", path=path)
        if not resp.ok:
            error_message = f"status_code: '{resp.status_code}' reason: '{resp.text}'"
            print(error_message)
            raise HandicapServiceFailure(error_message)

        results = resp.json().get('result')
        if not results:
            error_message = f"The user_id: {self.user_id} does not have any golf_round records"
            print(error_message)
            raise HandicapServiceFailure(error_message)
        golf_rounds = [GolfRound(**result) for result in results]
        return golf_rounds

    def _get_tee_box(self, tee_box_id: int) -> TeeBox:
        path = f"/golf-courses/tee-boxes/{tee_box_id}"
        resp = self.footwedge_api_client.call(method="get", path=path)
        if not resp.ok:
            error_message = f"status_code: '{resp.status_code}' reason: '{resp.text}'"
            print(error_message)
            raise HandicapServiceFailure(error_message)

        result = resp.json().get('result')
        if not result:
            error_message = f"No tee-box with id: {tee_box_id}"
            raise HandicapServiceFailure(error_message)
        return TeeBox(**result)

    @staticmethod
    def calculate_differential(gross_score: int, course_rating: Decimal, slope: Decimal) -> Decimal:
        differential = ((gross_score - course_rating) * 113) / slope
        return differential

    @staticmethod
    def determine_sample_size(num_rounds: int) -> int:
        if num_rounds < 5:
            error_message = 'sample size is too small, need atleast 5 rounds recorded'
            raise SampleSizeTooSmall(error_message)
        if num_rounds <= 10:
            size = 1
        elif num_rounds <= 19:
            size = 5
        else:
            size = 10

        return size

    def determine_lowest_differential(self, differentials: List[Decimal]) -> List[Decimal]:
        sample_size = self.determine_sample_size(num_rounds=len(differentials))
        num_differentials = len(differentials)
        if sample_size > num_differentials:
            error_message = f"sample_size: {sample_size} is greater than " \
                            f"the number of differentials: {num_differentials}"
            raise HandicapServiceFailure(error_message)
        elif sample_size == num_differentials:
            return differentials
        else:
            sorted_differentials = sorted(differentials)
            lowest_differentials = sorted_differentials[:sample_size]
            return lowest_differentials

    def calculate_handicap_index(self, differentials) -> Decimal:
        lowest_differentials = self.determine_lowest_differential(
            differentials=differentials,
        )
        handicap_index = (sum(lowest_differentials) / len(lowest_differentials)) * Decimal('0.96')
        return round(handicap_index, 1)

    def post_handicap(self):
        ordered_golf_rounds = self._get_golf_rounds()
        if len(ordered_golf_rounds) > 20:
            golf_rounds = ordered_golf_rounds[:20]
        else:
            golf_rounds = ordered_golf_rounds

        differentials = []
        for golf_round in golf_rounds:
            tee_box = self._get_tee_box(tee_box_id=golf_round.tee_box_id)
            differential = self.calculate_differential(
                gross_score=golf_round.gross_score,
                course_rating=tee_box.course_rating,
                slope=tee_box.slope,
            )
            differentials.append(differential)

        try:
            handicap_index = self.calculate_handicap_index(differentials=differentials)
        except (SampleSizeTooSmall, HandicapServiceFailure) as exc:
            print(exc)
            return

        data = {"index": handicap_index, "authorized_association": "USGA"}
        handicap_path = f"/handicaps/{self.user_id}"
        self.footwedge_api_client.call(
            method="post",
            path=handicap_path,
            json=json.loads(json.dumps(data, default=str)),
            headers={"Content-Type": "application/json"},
        )
