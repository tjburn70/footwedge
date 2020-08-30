from http import HTTPStatus

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from marshmallow import ValidationError

from api.schemas import (
    GolfRoundSchema,
    GolfRoundStatsSchema
)
from api.helpers import requires_json_content
from api import tasks
from api.repositories.golf_round_repository import golf_round_repo
from api.repositories.golf_round_stats_repository import golf_round_stats_repo


blueprint = Blueprint('golf-rounds', __name__)
golf_round_schema = GolfRoundSchema()
golf_round_stats_schema = GolfRoundStatsSchema()


@blueprint.route('/', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
def golf_rounds():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        rounds = golf_round_repo.get_by_user_id(user_id=user_id)
        results = golf_round_schema.dump(rounds, many=True)
        response_body = {
            'status': 'success',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    request_body = request.get_json()
    request_body['user_id'] = user_id
    try:
        golf_round_data = golf_round_schema.load(request_body).data
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    new_round = golf_round_repo.create(data=golf_round_data)
    golf_round_id = new_round.id

    celery_kwargs = {
        "queue": "handicap",
    }
    args = [user_id, ]
    tasks.calculate_usga_handicap.apply_async(args, **celery_kwargs)

    result = golf_round_schema.dump(new_round)
    response_body = {
        'status': 'success',
        'message': f"GolfRound: '{golf_round_id}' was successfully added for user_id: '{user_id}'",
        'result': result.data,
        'uri': f'/user/{user_id}/golf-rounds/{golf_round_id}',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/<int:golf_round_id>/golf-round-stats', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
def golf_round_stats(golf_round_id):
    user_id = get_jwt_identity()
    if request.method == 'GET':
        round_stats = golf_round_stats_repo.get_by_golf_round_id(golf_round_id=golf_round_id)
        results = golf_round_stats_schema.dump(round_stats, many=True)
        response_body = {
            'status': 'success',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    request_body = request.get_json()
    if not request_body.get('round_stats'):
        response_body = {
            'status': 'fail',
            'message': "Request is missing required parameter: 'round_stats'"
        }
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    round_stats = []
    for hole_stat in request_body.get('round_stats'):
        hole_stat['golf_round_id'] = golf_round_id
        try:
            round_stat_data = golf_round_stats_schema.load(hole_stat).data
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        round_stats.append(round_stat_data)

    golf_round_stats_repo.bulk_create(records=round_stats)
    results = golf_round_stats_schema.dump(round_stats, many=True)
    message = f"GolfRoundStats records were successfully added for GolfRound id: '{golf_round_id}'"
    response_body = {
        'status': 'success',
        'message': message,
        'uri': f'/users/{user_id}/golf-rounds/{golf_round_id}/golf-round-stats',
        'result': results.data,
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)
