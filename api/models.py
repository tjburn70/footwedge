from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from api.database import Base
from sqlalchemy import Column, Boolean, Integer, String, Date, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

DEFAULT_SCHEMA = 'public'


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), index=True, unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_initial = Column(String)
    phone_number = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    role = Column(String, nullable=False, default='standard_user')
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)
    handicaps = relationship('Handicap', backref='handicaps')
    profiles = relationship('Profile', backref='profiles')

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


class Profile(Base):
    __tablename__ = "profile"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('public.user.id'), nullable=False)
    home_course = Column(String)
    dexterity = Column(String)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)


class Handicap(Base):
    __tablename__ = "handicap"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('public.user.id'), nullable=False)
    index = Column(Numeric, nullable=False)
    authorized_association = Column(String, default='USGA')
    record_start_date = Column(DateTime, nullable=False, default=datetime.utcnow())
    record_end_date = Column(DateTime)


class GolfClub(Base):
    __tablename__ = "golf_club"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    address = Column(String)
    city = Column(String)
    state_code = Column(String)
    county = Column(String)
    zip_code = Column(String)
    phone_number = Column(String)
    email = Column(String)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)
    golf_courses = relationship('GolfCourse', backref='golf_courses')


class GolfCourse(Base):
    __tablename__ = "golf_course"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    golf_club_id = Column(Integer, ForeignKey('public.golf_club.id'), nullable=False)
    name = Column(String, nullable=False)
    num_holes = Column(Integer)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)
    tee_boxes = relationship('TeeBox', backref='tee_boxes')
    holes = relationship('Hole', backref='holes')


class TeeBox(Base):
    __tablename__ = "tee_box"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    golf_course_id = Column(Integer, ForeignKey('public.golf_course.id'), nullable=False)
    tee_color = Column(String)
    par = Column(Integer, nullable=False)
    distance = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    course_rating = Column(Numeric, nullable=False)
    slope = Column(Numeric, nullable=False)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)
    golf_holes = relationship('Hole', backref='golf_holes')


class Hole(Base):
    __tablename__ = "hole"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    golf_course_id = Column(Integer, ForeignKey('public.golf_course.id'), nullable=False)
    tee_box_id = Column(Integer, ForeignKey('public.tee_box.id'), nullable=False)
    name = Column(String, nullable=True)
    hole_number = Column(Integer, nullable=False)
    par = Column(Integer, nullable=False)
    handicap = Column(Integer, nullable=False)
    distance = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)
    round_stats = relationship('GolfRoundStats', backref='hole_round_stats')


class GolfRound(Base):
    __tablename__ = "golf_round"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    golf_course_id = Column(Integer, ForeignKey('public.golf_course.id'), nullable=False)
    tee_box_id = Column(Integer, ForeignKey('public.tee_box.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('public.user.id'), nullable=False)
    gross_score = Column(Integer, nullable=False)
    towards_handicap = Column(Boolean, nullable=False, default=True)
    played_on = Column(Date, nullable=False)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)
    stats = relationship('GolfRoundStats', backref='round_stats')


class GolfRoundStats(Base):
    __tablename__ = "golf_round_stats"
    __table_args__ = {'schema': DEFAULT_SCHEMA}
    id = Column(Integer, primary_key=True, autoincrement=True)
    golf_round_id = Column(Integer, ForeignKey('public.golf_round.id'), nullable=False)
    hole_id = Column(Integer, ForeignKey('public.hole.id'), nullable=False)
    gross_score = Column(Integer, nullable=False)
    fairway_hit = Column(Boolean)
    green_in_regulation = Column(Boolean, nullable=False)
    putts = Column(Integer, nullable=False, default=0)
    chips = Column(Integer, nullable=False, default=0)
    greenside_sand_shots = Column(Integer, nullable=False, default=0)
    penalties = Column(Integer, nullable=False, default=0)
    created_ts = Column(DateTime, nullable=False, default=datetime.utcnow())
    touched_ts = Column(DateTime)
