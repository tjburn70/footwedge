from datetime import datetime

from . import db, DEFAULT_SCHEMA


class GolfCourse(db.Model):
    __tablename__ = "golf_course"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    golf_club_id = db.Column(db.Integer, db.ForeignKey('public.golf_club.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    num_holes = db.Column(db.Integer)
    created_ts = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.Datetime)
    tee_boxes = db.relationship('TeeBox', backref='tee_boxes')

    def save(self):
        """
        Persist the GolfCourse in the database
        :param:
        :return: Id of GolfCourse record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing GolfCourse in the database
        :param:
        :return: Id of GolfCourse record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id
