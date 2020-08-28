from api.repositories.base_repository import BaseRepository
from api.models import GolfClub


class GolfClubRepository(BaseRepository):
    pass


golf_club_repo = GolfClubRepository(model=GolfClub)
