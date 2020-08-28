from api.repositories.base_repository import BaseRepository
from api.models import User


class UserRepository(BaseRepository):

    def get_by_email(self, email: str) -> User:
        """
        Filter a User by email.
        :param: email
        :return: User or None
        """
        return self.db_session.query(self.model).filter_by(email=email).first()


user_repo = UserRepository(model=User)
