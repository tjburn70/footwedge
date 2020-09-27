from typing import List

from api.repositories.base_repository import BaseRepository
from api.models import GolfRoundStats


class GolfRoundStatsRepository(BaseRepository):

    def get_by_golf_round_id(self, golf_round_id: int) -> List[GolfRoundStats]:
        """
        Retrieve all GolfRoundStats records by GolfRound id
        :param: user_id
        :return: List(GolfRoundStats) or empty list
        """
        return self.db_session.query(self.model).filter_by(golf_round_id=golf_round_id).all()


golf_round_stats_repo = GolfRoundStatsRepository(model=GolfRoundStats)
