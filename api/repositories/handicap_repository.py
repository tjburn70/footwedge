from datetime import datetime
from typing import List

from api.repositories.base_repository import BaseRepository
from api.models import Handicap


class HandicapRepository(BaseRepository):

    def close(self, model_obj: Handicap):
        """
        Close out an old Handicap record
        :param:
        :return: Handicap record just closed
        """
        model_obj.record_end_date = datetime.now()
        self.db_session.merge(model_obj)
        self.db_session.commit()
        self.db_session.refresh(model_obj)
        return model_obj

    def get_active(self, user_id: int) -> Handicap:
        """
        Query a User's active Handicap by their user id
        :param: user_id
        :return: Handicap or None
        """
        return self.db_session.query(self.model)\
            .filter_by(record_end_date=None)\
            .filter(self.model.user_id == user_id)\
            .first()

    def get_by_date(self, user_id: int, start_date: datetime) -> List[Handicap]:
        """
        Query all User's Handicaps greater than a given date
        :param: user_id, start_date
        :return: list(Handicap) or empty list
        """
        return self.db_session.query(self.model)\
            .filter(self.model.user_id == user_id)\
            .filter(self.model.record_start_date >= start_date)\
            .all()

    def get_all_by_user(self, user_id: int) -> List[Handicap]:
        """
        Get all Handicap records for a User
        :param: user_id
        :return: Handicap or None
        """
        return self.db_session.query(self.model).filter(self.model.user_id == user_id).all()


handicap_repo = HandicapRepository(model=Handicap)
