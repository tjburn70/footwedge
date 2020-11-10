from flask import (
    Blueprint,
    request
)

from api.services import (
    golf_course_service,
    golf_club_service,
)
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
    service = golf_club_service.GolfClubService(
        repo=golf_club_repo,
        schema=golf_club_schema,
    )
    if request.method == 'GET':
        return service.get_all()

    return service.add(payload=request.get_json())


@blueprint.route('/<int:golf_club_id>', methods=['GET', 'DELETE'])
@throws_500_on_exception
def golf_clubs_by_id(golf_club_id):
    service = golf_club_service.GolfClubService(
        repo=golf_club_repo,
        schema=golf_club_schema,
    )
    if request.method == 'GET':
        return service.get(_id=golf_club_id)
    if request.method == 'DELETE':
        return service.delete(_id=golf_club_id)


@blueprint.route('/<int:golf_club_id>/golf-courses', methods=['GET', 'POST'])
@throws_500_on_exception
def golf_courses(golf_club_id):
    service = golf_course_service.GolfCourseService(
        repo=golf_course_repo,
        schema=golf_course_schema,
    )
    if request.method == 'GET':
        return service.get_by_golf_club_id(golf_club_id=golf_club_id)

    request_body = request.get_json()
    request_body['golf_club_id'] = golf_club_id
    return service.add(payload=request_body)
