from api.repositories.base_repository import BaseRepository
from api.models import User
from api.schemas import UserSchema

user_schema = UserSchema()


class UserRepository(BaseRepository):

    def get_by_email(self, email: str) -> User:
        """
        Filter a User by email.
        :param: email
        :return: User or None
        """
        return self.db_session.query(self.model).filter_by(email=email).first()

    def reset_password(self, user_obj: User, new_password: str) -> User:
        """
        Update/reset the user password.
        :param: user_obj
        :param: new_password
        :return: User
        """
        user_obj.password_hash = User.hash_password(password=new_password)
        user_data = user_schema.dump(user_obj)
        return self.update(data=user_data)


user_repo = UserRepository(model=User)
