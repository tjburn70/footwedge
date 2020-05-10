from marshmallow import Schema, fields


class HandicapSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    index = fields.Decimal(required=True)
    authorized_association = fields.Str()
    record_start_date = fields.DateTime(dump_only=True)
    record_end_date = fields.DateTime()


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
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class GolfCourseSchema(Schema):
    id = fields.Int(dump_only=True)
    golf_club_id = fields.Int(required=True)
    name = fields.Str(required=True)
    num_holes = fields.Int()
    created_ts = fields.DateTime(dump_only=True)
    touched_ts = fields.DateTime()


class TeeBoxSchema(Schema):
    id = fields.Int(dump_only=True)
    golf_course_id = fields.Int(required=True)
    tee_color = fields.Str()
    par = fields.Int()
    distance = fields.Int()
    unit = fields.Str()
    course_rating = fields.Decimal()
    slope = fields.Decimal()
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
