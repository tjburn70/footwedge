from datetime import datetime

from . import db, DEFAULT_SCHEMA


class TeeBox(db.Model):
    __tablename__ = "tee_box"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    golf_course_id = db.Column(db.Integer, db.ForeignKey('public.golf_course.id'), nullable=False)
    tee_color = db.Column(db.String)
    par = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String, nullable=False)
    course_rating = db.Column(db.Numeric, nullable=False)
    slope = db.Column(db.Numeric, nullable=False)
    created_ts = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.Datetime)
    golf_holes = db.relationship('Hole', backref='golf_holes')

    def save(self):
        """
        Persist the TeeBox in the database
        :param:
        :return: Id of TeeBox record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing TeeBox in the database
        :param:
        :return: Id of TeeBox record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id
