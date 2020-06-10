from http import HTTPStatus

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)
from marshmallow import ValidationError

from api.models import (
    GolfClub,
    GolfCourse,
)
from api.schemas import (
    GolfClubSchema,
    GolfCourseSchema,
)
from api.helpers import (
    requires_json_content,
    throws_500_on_exception,
)


blueprint = Blueprint('golf-clubs', __name__)
golf_club_schema = GolfClubSchema()
golf_course_schema = GolfCourseSchema()


@blueprint.route('/', methods=['GET', 'POST'])
@requires_json_content
@throws_500_on_exception
def golf_clubs():
    if request.method == 'GET':
        clubs = GolfClub.get_all()
        results = golf_club_schema.dump(clubs, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    try:
        request_body = request.get_json()
        result = golf_club_schema.load(request_body)
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    club = GolfClub(**result.data)
    club_id = club.save()
    response_body = {
        'status': 'success',
        'message': f"Golf Club: '{club.name}' was successfully added",
        'uri': f'api/golf-clubs/{club_id}',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/<int:golf_club_id>', methods=['GET'])
@throws_500_on_exception
def golf_clubs_by_id(golf_club_id):
    golf_club = GolfClub.get_by_id(golf_club_id=golf_club_id)
    if not golf_club:
        response_body = {
            'status': 'fail',
            'message': f"No GolfClub exists with id: '{golf_club_id}'"
        }
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    result = golf_club_schema.dump(golf_club)
    response_body = {
        'status': 'success',
        'result': result.data
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/<int:golf_club_id>/golf-courses', methods=['GET', 'POST'])
@throws_500_on_exception
def golf_courses(golf_club_id):
    if request.method == 'GET':
        courses = GolfCourse.get_by_golf_club_id(golf_club_id=golf_club_id)
        if not courses:
            response_body = {
                'status': 'fail',
                'message': f"No GolfCourse exists with GolfClub id: '{golf_club_id}'"
            }
            return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)
        else:
            results = golf_course_schema.dump(courses, many=True)
            response_body = {
                'status': 'success',
                'result': results.data
            }
            return make_response(jsonify(response_body), HTTPStatus.OK.value)

    try:
        request_body = request.get_json()
        request_body['golf_club_id'] = golf_club_id
        result = golf_course_schema.load(request_body)
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    course = GolfCourse(**result.data)
    course_id = course.save()
    response_body = {
        'status': 'success',
        'message': f"Golf Course: '{course.name}' was successfully added",
        'uri': f'api/golf-clubs/{golf_club_id}/golf-courses/{course_id}',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)
