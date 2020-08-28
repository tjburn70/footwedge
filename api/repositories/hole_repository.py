from typing import List

from api.repositories.base_repository import BaseRepository
from api.models import Hole


class HoleRepository(BaseRepository):

    def get_by_golf_course_id(self, golf_course_id: int) -> List[Hole]:
        """
        Retrieve all Hole by GolfCourse id.
        :param: golf_course_id
        :return: List(Hole) or empty list
        """
        return self.db_session.query(self.model).filter_by(golf_course_id=golf_course_id).all()

    def get_by_tee_box_id(self, tee_box_id: int) -> list:
        """
        Retrieve all Hole records by TeeBox id
        :param: tee_box_id
        :return: List(Hole) or empty list
        """
        return self.db_session.query(self.model).filter_by(tee_box_id=tee_box_id).all()

    # TODO: bulk save?


hole_repo = HoleRepository(model=Hole)
