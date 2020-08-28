from typing import List

from api.repositories.base_repository import BaseRepository
from api.models import GolfRound


class GolfRoundRepository(BaseRepository):

    def get_by_user_id(self, user_id: int) -> List[GolfRound]:
        """
        Retrieve all GolfRound records by User id
        :param: user_id
        :return: List(GolfRound) or empty list
        """
        return self.db_session.query(self.model).filter_by(user_id=user_id).order_by(GolfRound.played_on.desc()).all()


golf_round_repo = GolfRoundRepository(model=GolfRound)
