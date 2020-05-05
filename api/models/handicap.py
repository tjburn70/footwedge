from datetime import datetime

from . import db, DEFAULT_SCHEMA

DEFAULT_AUTHORIZED_ASSOCIATION = 'USGA'


class Handicap(db.Model):
    __tablename__ = "handicap"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.user_id'), nullable=False)
    index = db.Column(db.Numeric, nullable=False)
    authorized_association = db.Column(db.String, default=DEFAULT_AUTHORIZED_ASSOCIATION)
    record_start_date = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    record_end_date = db.Column(db.Datetime)

    def save(self):
        """
        Persist the Handicap in the database
        :param:
        :return: Id of Handicap record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def close(self):
        """
        Close out an old Handicap record
        :param:
        :return: Id of Handicap record just closed
        """
        self.record_end_date = datetime.now()
        db.session.merge(self)
        db.session.commit()
        return self.id

    @staticmethod
    def get_active(user_id):
        """
        Query a User's active Handicap by their user id
        :param: user_id
        :return: User or None
        """
        return Handicap.query.filter_by(user_id=user_id, record_end_date=None).first()

    @staticmethod
    def get_all(user_id):
        """
        Query a User's active Handicap by their user id
        :param: user_id
        :return: User or None
        """
        return Handicap.query.filter_by(user_id=user_id).all()
