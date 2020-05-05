from datetime import datetime

from . import db, DEFAULT_SCHEMA


class GolfClub(db.Model):
    __tablename__ = "golf_club"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state_code = db.Column(db.String)
    county = db.Column(db.String)
    zip_code = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    created_ts = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.Datetime)
    golf_courses = db.relationship('GolfCourse', backref='golf_courses')

    def save(self):
        """
        Persist the GolfClub in the database
        :param:
        :return: Id of GolfClub record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing GolfClub in the database
        :param:
        :return: Id of GolfClub record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id
