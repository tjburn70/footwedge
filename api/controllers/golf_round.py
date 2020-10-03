from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from api.services import (
    golf_round_service,
    golf_round_stats_service,
    hole_service,
)
from api.repositories.golf_round_repository import golf_round_repo
from api.repositories.golf_round_stats_repository import golf_round_stats_repo
from api.repositories.hole_repository import hole_repo
from api.schemas import (
    GolfRoundSchema,
    GolfRoundStatsSchema,
    HoleSchema
)
from api.helpers import requires_json_content


blueprint = Blueprint('golf-rounds', __name__)
golf_round_schema = GolfRoundSchema()
golf_round_stats_schema = GolfRoundStatsSchema()
hole_schema = HoleSchema()


@blueprint.route('/', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
def golf_rounds():
    user_id = get_jwt_identity()
    service = golf_round_service.GolfRoundService(
        repo=golf_round_repo,
        schema=golf_round_schema,
    )
    if request.method == 'GET':
        return service.get_by_user_id(user_id=user_id)

    payload = request.get_json()
    return service.add(user_id=user_id, payload=payload)


@blueprint.route('/<int:user_id>', methods=['GET'])
@requires_json_content
def golf_rounds_by_user_id(user_id):
    # TODO: Implement Authentication for server to server auth
    service = golf_round_service.GolfRoundService(
        repo=golf_round_repo,
        schema=golf_round_schema,
    )
    return service.get_by_user_id(user_id=user_id)


@blueprint.route('/<int:golf_round_id>/golf-round-stats', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
def golf_round_stats(golf_round_id):
    service = golf_round_stats_service.GolfRoundStatsService(
        repo=golf_round_stats_repo,
        schema=golf_round_stats_schema,
    )
    if request.method == 'GET':
        return service.get_by_golf_round_id(golf_round_id=golf_round_id)

    payload = request.get_json()
    return service.add(golf_round_id=golf_round_id, payload=payload)


@blueprint.route('/golf-round-stats/summary', methods=['GET'])
@requires_json_content
@jwt_required
def stats_summary():
    user_id = get_jwt_identity()
    stats_service = golf_round_stats_service.GolfRoundStatsService(
        repo=golf_round_stats_repo,
        schema=golf_round_stats_schema,
    )
    rounds = golf_round_repo.get_by_user_id(user_id=user_id)
    hole_svc = hole_service.HoleService(
        repo=hole_repo,
        schema=hole_schema,
    )
    return stats_service.stats_summary_by_round_id(golf_rounds=rounds, hole_service=hole_svc)
