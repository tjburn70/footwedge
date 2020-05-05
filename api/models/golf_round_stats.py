from datetime import datetime

from . import db, DEFAULT_SCHEMA


class GolfRoundStats(db.Model):
    __tablename__ = "golf_round_stats"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    golf_round_id = db.Column(db.Integer, db.ForeignKey('public.golf_round.id'), nullable=False)
    hole_id = db.Column(db.Integer, db.ForeignKey('public.hole.id'), nullable=False)
    gross_score = db.Column(db.Integer, nullable=False)
    fairway_hit = db.Column(db.Boolean)
    green_in_regulation = db.Column(db.Boolean, nullable=False)
    putts = db.Column(db.Integer, nullable=False, default=0)
    chips = db.Column(db.Integer, nullable=False, default=0)
    greenside_sand_shots = db.Column(db.Integer, nullable=False, default=0)
    penalties = db.Column(db.Integer, nullable=False, default=0)
    created_ts = db.Column(db.Datetime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.Datetime)

    def save(self):
        """
        Persist the GolfRoundStats in the database
        :param:
        :return: Id of GolfRoundStats record
        """
        db.session.add(self)
        db.session.commit()
        return self.id

    def update(self):
        """
        Update an existing GolfRoundStats in the database
        :param:
        :return: Id of GolfRoundStats record
        """
        db.session.merge(self)
        db.session.commit()
        return self.id
