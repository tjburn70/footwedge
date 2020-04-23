from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from . import db

# TODO enum for roles - admin, standard_user, premium_user


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    middle_initial = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String)
    role = db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, email, password, **kwargs):
        self.email = email
        self.password_hash = User.hash_password(password)
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.middle_initial = kwargs.get('middle_initial')
        self.phone_number = kwargs.get('phone_number')
        self.date_of_birth = kwargs.get('date_of_birth')
        self.gender = kwargs.get('gender')
        self.role = kwargs.get('role')
        self.registered_on = datetime.now()

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        """
        Persist the user in the database
        :param:
        :return: Id of User record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing the user in the database
        :param:
        :return: Id of User record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id(user_id):
        """
        Filter a user by Id.
        :param user_id:
        :return: User or None
        """
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        """
        Check a user by their email address
        :param: email
        :return: User or None
        """
        return User.query.filter_by(email=email).first()

    def reset_password(self, new_password):
        """
        Update/reset the user password.
        :param: new_password New User Password
        :return:
        """
        self.password_hash = User.hash_password(password=new_password)
        self.save()
