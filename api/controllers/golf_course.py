from flask import (
    Blueprint,
    request
)

from api.services import (
    golf_course_service,
    tee_box_service,
    hole_service,
)
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
    service = golf_course_service.GolfCourseService(
        repo=golf_course_repo,
        schema=golf_course_schema,
    )
    if ids:
        return service.get_by_ids(ids=ids)

    return service.get_all()


@blueprint.route('/<int:golf_course_id>', methods=['GET', 'DELETE'])
@throws_500_on_exception
def golf_courses_by_id(golf_course_id):
    service = golf_course_service.GolfCourseService(
        repo=golf_course_repo,
        schema=golf_course_schema,
    )
    if request.method == 'GET':
        return service.get(_id=golf_course_id)
    if request.method == 'DELETE':
        return service.delete(_id=golf_course_id)


@blueprint.route('/<int:golf_course_id>/tee-boxes', methods=['GET', 'POST'])
@requires_json_content
@throws_500_on_exception
def tee_boxes(golf_course_id):
    service = tee_box_service.TeeBoxService(
        repo=tee_box_repo,
        schema=tee_box_schema,
    )
    if request.method == 'GET':
        return service.get_by_golf_course_id(golf_course_id=golf_course_id)

    payload = request.get_json()
    return service.add(golf_course_id=golf_course_id, payload=payload)


# TODO: Consider diff controller?
@blueprint.route('/tee-boxes/<int:tee_box_id>', methods=['GET', 'DELETE'])
@throws_500_on_exception
def tee_box_by_id(tee_box_id):
    service = tee_box_service.TeeBoxService(
        repo=tee_box_repo,
        schema=tee_box_schema,
    )
    if request.method == 'GET':
        return service.get(_id=tee_box_id)
    if request.method == 'DELETE':
        return service.delete(_id=tee_box_id)


@blueprint.route('/<int:golf_course_id>/tee-boxes/<int:tee_box_id>/holes', methods=['GET', 'POST'])
@requires_json_content
@throws_500_on_exception
def holes(golf_course_id, tee_box_id):
    service = hole_service.HoleService(
        repo=hole_repo,
        schema=hole_schema,
    )
    if request.method == 'GET':
        return service.get_by_tee_box_id(tee_box_id=tee_box_id)

    payload = request.get_json()
    return service.add(
        golf_course_id=golf_course_id,
        tee_box_id=tee_box_id,
        payload=payload
    )
