from typing import List

from api.repositories.base_repository import BaseRepository
from api.models import TeeBox


class TeeBoxRepository(BaseRepository):

    def get_by_golf_course_id(self, golf_course_id: int) -> List[TeeBox]:
        """
        Filter a TeeBox by GolfCourse id.
        :param: golf_course_id
        :return: List(TeeBox) or empty list
        """
        return self.db_session.query(self.model).filter_by(golf_course_id=golf_course_id).all()


tee_box_repo = TeeBoxRepository(model=TeeBox)
