from marshmallow import Schema, fields


class HandicapSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    index = fields.Decimal(required=True, as_string=True)
    authorized_association = fields.Str()
    record_start_date = fields.DateTime(dump_only=True)
    record_end_date = fields.DateTime()


class TeeBoxSchema(Schema):
    id = fields.Int(dump_only=True)
    golf_course_id = fields.Int(required=True)
    tee_color = fields.Str()
    par = fields.Int()
    distance = fields.Int()
    unit = fields.Str()
    course_rating = fields.Decimal(as_string=True)
    slope = fields.Decimal(as_string=True)
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class GolfCourseSchema(Schema):
    id = fields.Int(dump_only=True)
    golf_club_id = fields.Int(required=True)
    name = fields.Str(required=True)
    num_holes = fields.Int()
    tee_boxes = fields.List(fields.Nested(TeeBoxSchema))
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class GolfClubSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str()
    city = fields.Str()
    state_code = fields.Str()
    county = fields.Str()
    zip_code = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    golf_courses = fields.List(fields.Nested(GolfCourseSchema))
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class HoleSchema(Schema):
    id = fields.Int(dump_only=True)
    golf_course_id = fields.Int(required=True)
    tee_box_id = fields.Int(required=True)
    name = fields.Str()
    hole_number = fields.Int(required=True)
    par = fields.Int(required=True)
    handicap = fields.Int(required=True)
    distance = fields.Int(required=True)
    unit = fields.Str(required=True)
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class GolfRoundStatsSchema(Schema):
    id = fields.Int(dump_only=True)
    golf_round_id = fields.Int(required=True)
    hole_id = fields.Int(required=True)
    gross_score = fields.Int(required=True)
    fairway_hit = fields.Boolean()
    green_in_regulation = fields.Boolean(required=True)
    putts = fields.Integer()
    chips = fields.Integer()
    greenside_sand_shots = fields.Integer()
    penalties = fields.Integer()
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class GolfRoundSchema(Schema):
    id = fields.Int(dump_only=True)
    golf_course_id = fields.Int(required=True)
    tee_box_id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    gross_score = fields.Int(required=True)
    towards_handicap = fields.Boolean()
    played_on = fields.Date(required=True)
    stats = fields.List(fields.Nested(GolfRoundStatsSchema))
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Str(required=True)
    password_hash = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    middle_initial = fields.Str()
    phone_number = fields.Str()
    date_of_birth = fields.Date()
    gender = fields.Str()
    role = fields.Str()
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()
