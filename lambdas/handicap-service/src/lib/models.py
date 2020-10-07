from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class GolfRound(BaseModel):
    id: int
    golf_course_id: int
    tee_box_id: int
    user_id: int
    gross_score: int
    towards_handicap: bool
    played_on: date


class TeeBox(BaseModel):
    id: int
    golf_course_id: int
    tee_color: str
    par: int
    distance: int
    unit: str
    course_rating: Decimal
    slope: Decimal
