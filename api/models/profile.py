from datetime import datetime

from . import db, DEFAULT_SCHEMA


class Profile(db.Model):
    __tablename__ = "profile"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.id'), nullable=False)
    home_course = db.Column(db.String)
    dexterity = db.Column(db.String)
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)

    def save(self):
        """
        Persist the User's Profile in the database
        :param:
        :return: Id of Profile record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing user profile in the database
        :param:
        :return: Id of Profile record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_by_id(user_id):
        """
        Query a User's Profile by their user id
        :param: user_id
        :return: User or None
        """
        return Profile.query.filter_by(user_id=user_id).first()
