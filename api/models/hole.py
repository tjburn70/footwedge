from datetime import datetime

from . import db, DEFAULT_SCHEMA


class Hole(db.Model):
    __tablename__ = "hole"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tee_box_id = db.Column(db.Integer, db.ForeignKey('public.tee_box.id'), nullable=False)
    hole_number = db.Column(db.Integer, nullable=False)
    par = db.Column(db.Integer, nullable=False)
    handicap = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String, nullable=False)
    created_ts = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.Datetime)
    round_stats = db.relationship('GolfRoundStats', backref='round_stats')

    def save(self):
        """
        Persist the Hole in the database
        :param:
        :return: Id of Hole record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing Hole in the database
        :param:
        :return: Id of Hole record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id
