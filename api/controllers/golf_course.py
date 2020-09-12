from http import HTTPStatus

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)
from marshmallow import ValidationError

from api.repositories.golf_course_repository import golf_course_repo
from api.repositories.tee_box_repository import tee_box_repo
from api.repositories.hole_repository import hole_repo
from api.schemas import (
    GolfCourseSchema,
    TeeBoxSchema,
    HoleSchema,
)
from api.helpers import (
    requires_json_content,
    throws_500_on_exception,
)


blueprint = Blueprint('golf-courses', __name__)
golf_course_schema = GolfCourseSchema()
tee_box_schema = TeeBoxSchema()
hole_schema = HoleSchema()


@blueprint.route('/', methods=['GET'])
@throws_500_on_exception
def golf_courses():
    ids = request.args.getlist('id')
    if ids:
        courses = golf_course_repo.get_by_ids(ids=ids)
        results = golf_course_schema.dump(courses, many=True)
        response_body = {
            'status': 'success',
            'result': results.data
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    courses = golf_course_repo.get_all()
    results = golf_course_schema.dump(courses, many=True)
    response_body = {
        'status': 'success',
        'result': results.data
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/<int:golf_course_id>', methods=['GET'])
@throws_500_on_exception
def golf_courses_by_id(golf_course_id):
    golf_course = golf_course_repo.get(golf_course_id)
    if not golf_course:
        response_body = {
            'status': 'fail',
            'message': f"No GolfCourse exists with id: '{golf_course_id}'"
        }
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    result = golf_course_schema.dump(golf_course)
    response_body = {
        'status': 'success',
        'result': result
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/<int:golf_course_id>/tee-boxes', methods=['GET', 'POST'])
@requires_json_content
@throws_500_on_exception
def tee_boxes(golf_course_id):
    if request.method == 'GET':
        boxes = tee_box_repo.get_by_golf_course_id(golf_course_id=golf_course_id)
        if not boxes:
            response_body = {
                'status': 'fail',
                'message': f"No TeeBoxes exists with GolfCourse id: '{golf_course_id}'"
            }
            return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)
        else:
            results = tee_box_schema.dump(boxes, many=True)
            response_body = {
                'status': 'success',
                'result': results.data
            }
            return make_response(jsonify(response_body), HTTPStatus.OK.value)

    request_body = request.get_json()
    request_body['golf_course_id'] = golf_course_id
    try:
        tee_box_data = tee_box_schema.load(request_body).data
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    tee_box = tee_box_repo.create(data=tee_box_data)
    tee_box_id = tee_box.id
    response_body = {
        'status': 'success',
        'message': f"Tee Box: '{tee_box.tee_color}' was successfully added",
        'uri': f'/golf-courses/{golf_course_id}/tee-boxes/{tee_box_id}',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


# TODO: Consider diff controller?
@blueprint.route('/tee-boxes/<int:tee_box_id>', methods=['GET'])
@throws_500_on_exception
def tee_box_by_id(tee_box_id):
    box = tee_box_repo.get(id=tee_box_id)
    if not box:
        response_body = {
            'status': 'fail',
            'message': f"No TeeBox exists with id: '{tee_box_id}'"
        }
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    data = tee_box_schema.dump(box).data
    response_body = {
        'status': 'success',
        'result': data
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/<int:golf_course_id>/tee-boxes/<int:tee_box_id>/holes', methods=['GET', 'POST'])
@requires_json_content
@throws_500_on_exception
def holes(golf_course_id, tee_box_id):
    if request.method == 'GET':
        hole_records = hole_repo.get_by_tee_box_id(tee_box_id=tee_box_id)
        if not hole_records:
            response_body = {
                'status': 'fail',
                'message': f"No Holes exist for TeeBox id: '{tee_box_id}'"
            }
            return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)
        else:
            results = hole_schema.dump(hole_records, many=True)
            response_body = {
                'status': 'success',
                'result': results.data
            }
            return make_response(jsonify(response_body), HTTPStatus.OK.value)

    request_body = request.get_json()
    if not request_body.get('holes'):
        response_body = {
            'status': 'fail',
            'message': "Request is missing required parameter: 'holes'"
        }
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    holes_data = []
    for hole in request_body.get('holes'):
        hole['golf_course_id'] = golf_course_id
        hole['tee_box_id'] = tee_box_id
        try:
            hole_data = hole_schema.load(hole).data
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        holes_data.append(hole_data)

    hole_repo.bulk_create(records=holes_data)

    message = "Hole records were successfully added for" \
              f" GolfCourse id: {golf_course_id} and TeeBox id: {tee_box_id}"
    response_body = {
        'status': 'success',
        'message': message,
        'uri': f'/golf-courses/{golf_course_id}/tee-boxes/{tee_box_id}/holes/',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)
