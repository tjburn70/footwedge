from http import HTTPStatus

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)
from marshmallow import ValidationError

from api.repositories.golf_club_repository import golf_club_repo
from api.repositories.golf_course_repository import golf_course_repo
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
        clubs = golf_club_repo.get_all()
        results = golf_club_schema.dump(clubs, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    request_body = request.get_json()
    try:
        golf_club_data = golf_club_schema.load(request_body).data
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    club = golf_club_repo.create(data=golf_club_data)
    club_id = club.id
    response_body = {
        'status': 'success',
        'message': f"Golf Club: '{club.name}' was successfully added",
        'uri': f'api/golf-clubs/{club_id}',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/<int:golf_club_id>', methods=['GET'])
@throws_500_on_exception
def golf_clubs_by_id(golf_club_id):
    golf_club = golf_club_repo.get(golf_club_id)
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
        courses = golf_course_repo.get_by_golf_club_id(golf_club_id=golf_club_id)
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

    request_body = request.get_json()
    request_body['golf_club_id'] = golf_club_id
    try:
        golf_course_data = golf_course_schema.load(request_body).data
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    course = golf_course_repo.create(data=golf_course_data)
    course_id = course.id
    response_body = {
        'status': 'success',
        'message': f"Golf Course: '{course.name}' was successfully added",
        'uri': f'api/golf-clubs/{golf_club_id}/golf-courses/{course_id}',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)
