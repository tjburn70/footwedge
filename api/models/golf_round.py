from datetime import datetime

from . import db, DEFAULT_SCHEMA


class GolfRound(db.Model):
    __tablename__ = "golf_round"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    golf_course_id = db.Column(db.Integer, db.ForeignKey('public.golf_course.id'), nullable=False)
    tee_box_id = db.Column(db.Integer, db.ForeignKey('public.tee_box.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.id'), nullable=False)
    gross_score = db.Column(db.Integer, nullable=False)
    towards_handicap = db.Column(db.Boolean, nullable=False, default=True)
    played_on = db.Column(db.Date, nullable=False)
    created_ts = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.Datetime)
    round_stats = db.relationship('GolfRoundStats', backref='round_stats')

    def save(self):
        """
        Persist the GolfRound in the database
        :param:
        :return: Id of GolfRound record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing GolfRound in the database
        :param:
        :return: Id of GolfRound record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id
