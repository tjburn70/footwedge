from typing import List

from api.repositories.base_repository import BaseRepository
from api.models import GolfCourse


class GolfCourseRepository(BaseRepository):

    def get_by_golf_club_id(self, golf_club_id: int) -> List[GolfCourse]:
        """
        Filter a GolfCourse by GolfClub id.
        :param: golf_course_id
        :return: List(GolfCourse) or empty list
        """
        return self.db_session.query(self.model).filter_by(golf_club_id=golf_club_id).all()


golf_course_repo = GolfCourseRepository(model=GolfCourse)
