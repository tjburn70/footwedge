from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_SCHEMA = 'public'


class User(db.Model):
    __tablename__ = "user"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    middle_initial = db.Column(db.String)
    phone_number = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String)
    role = db.Column(db.String, nullable=False, default='standard_user')
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)
    handicaps = db.relationship('Handicap', backref='handicaps')
    profiles = db.relationship('Profile', backref='profiles')

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password_hash = User.hash_password(kwargs.get('password'))
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.middle_initial = kwargs.get('middle_initial')
        self.phone_number = kwargs.get('phone_number')
        self.date_of_birth = kwargs.get('date_of_birth')
        self.gender = kwargs.get('gender')
        self.role = kwargs.get('role')
        self.created_ts = kwargs.get('created_ts')
        self.touched_ts = kwargs.get('touched_ts')

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


class Handicap(db.Model):
    __tablename__ = "handicap"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('public.user.id'), nullable=False)
    index = db.Column(db.Numeric, nullable=False)
    authorized_association = db.Column(db.String, default='USGA')
    record_start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    record_end_date = db.Column(db.DateTime)

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
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)
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

    @staticmethod
    def get_by_id(golf_club_id):
        """
        Filter a GolfClub by Id.
        :param: golf_club_id
        :return: GolfClub or None
        """
        return GolfClub.query.filter_by(id=golf_club_id).first()

    @staticmethod
    def get_all():
        """
        Retrieve all GolfClub records
        :param: None
        :return: GolfClubs or empty list
        """
        return GolfClub.query.all()


class GolfCourse(db.Model):
    __tablename__ = "golf_course"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    golf_club_id = db.Column(db.Integer, db.ForeignKey('public.golf_club.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    num_holes = db.Column(db.Integer)
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)
    tee_boxes = db.relationship('TeeBox', backref='tee_boxes')
    holes = db.relationship('Hole', backref='holes')

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

    @staticmethod
    def get_by_id(golf_course_id: int):
        """
        Filter a GolfCourse by id.
        :param: golf_course_id
        :return: GolfCourse or None
        """
        return GolfCourse.query.filter_by(id=golf_course_id).first()

    @staticmethod
    def get_by_golf_club_id(golf_club_id: int) -> list:
        """
        Filter a GolfCourse by GolfClub id.
        :param: golf_course_id
        :return: List(GolfCourse) or empty list
        """
        return GolfCourse.query.filter_by(golf_club_id=golf_club_id).all()


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
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)
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

    @staticmethod
    def get_by_golf_course_id(golf_course_id: int) -> list:
        """
        Filter a TeeBox by GolfCourse id.
        :param: golf_course_id
        :return: List(TeeBox) or empty list
        """
        return TeeBox.query.filter_by(golf_course_id=golf_course_id).all()


class Hole(db.Model):
    __tablename__ = "hole"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    golf_course_id = db.Column(db.Integer, db.ForeignKey('public.golf_course.id'), nullable=False)
    tee_box_id = db.Column(db.Integer, db.ForeignKey('public.tee_box.id'), nullable=False)
    hole_number = db.Column(db.Integer, nullable=False)
    par = db.Column(db.Integer, nullable=False)
    handicap = db.Column(db.Integer, nullable=False)
    distance = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String, nullable=False)
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)
    round_stats = db.relationship('GolfRoundStats', backref='hole_round_stats')

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

    @staticmethod
    def get_by_golf_course_id(golf_course_id: int) -> list:
        """
        Retrieve all Hole records by GolfCourse id
        :param: golf_course_id
        :return: List(Hole) or empty list
        """
        return Hole.query.filter_by(golf_course_id=golf_course_id).all()

    @staticmethod
    def get_by_tee_box_id(tee_box_id: int) -> list:
        """
        Retrieve all Hole records by TeeBox id
        :param: tee_box_id
        :return: List(Hole) or empty list
        """
        return Hole.query.filter_by(tee_box_id=tee_box_id).all()


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
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)
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
    created_ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = db.Column(db.DateTime)

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
