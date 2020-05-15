from http import HTTPStatus

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jti,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required,
)
from marshmallow import ValidationError

from api.config import REFRESH_EXPIRES
from api.controllers import auth
from api.models import (
    User,
    Handicap,
    GolfRound,
    GolfRoundStats,
)
from api.schemas import (
    HandicapSchema,
    GolfRoundSchema,
    GolfRoundStatsSchema
)
from api.helpers import (
    requires_json_content,
    throws_500_on_exception,
)


blueprint = Blueprint('user', __name__)
handicap_schema = HandicapSchema()
golf_round_schema = GolfRoundSchema()
golf_round_stats_schema = GolfRoundStatsSchema()


@blueprint.route('/register', methods=['POST'])
@throws_500_on_exception
@requires_json_content
def register_user():
    request_body = request.get_json()
    email = request_body.get('email')
    password = request_body.get('password')

    if not email or not password:
        error_message = "Missing required parameters: 'email' and/or 'password'"
        response_body = {"message": error_message}
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    if User.get_by_email(email):
        error_message = f"A user with email: '{email}' already exists!"
        response_body = {"message": error_message}
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    new_user = User(**request_body)
    user_id = new_user.save()
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    refresh_jti = get_jti(encoded_token=refresh_token)
    auth.redis_client.set(
        name=refresh_jti,
        value=auth.ACTIVE_TOKEN_FLAG,
        ex=REFRESH_EXPIRES
    )

    response_body = {
        "status": "success",
        "message": "user is registered",
        "user_id": user_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    return make_response(jsonify(response_body), HTTPStatus.CREATED.OK)


@blueprint.route('/login', methods=['POST'])
@throws_500_on_exception
@requires_json_content
def login():
    request_body = request.get_json()
    email = request_body.get('email')
    password = request_body.get('password')

    if not email or not password:
        error_message = "Missing required parameters: email and/or password"
        response_body = {"message": error_message}
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    current_user = User.get_by_email(email)
    if not current_user:
        error_message = f"No user exists with email: '{email}'"
        response_body = {"message": error_message}
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    valid_password = current_user.verify_password(password)
    if valid_password:
        access_token = create_access_token(identity=current_user.id)
        refresh_token = create_refresh_token(identity=current_user.id)
        refresh_jti = get_jti(encoded_token=refresh_token)
        auth.redis_client.set(
            name=refresh_jti,
            value=auth.ACTIVE_TOKEN_FLAG,
            ex=REFRESH_EXPIRES
        )
        response_body = {
            "status": "success",
            "message": "user is logged in",
            "user_id": current_user.id,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)
    else:
        error_message = f"Invalid password for email: {email}"
        response_body = {"message": error_message}
        return make_response(jsonify(response_body), HTTPStatus.UNAUTHORIZED.value)


@blueprint.route('/logout', methods=['DELETE'])
@jwt_refresh_token_required
def logout():
    jti = get_raw_jwt()['jti']
    auth.redis_client.set(
        name=jti,
        value=auth.BLACKLISTED_TOKEN_FLAG,
        ex=REFRESH_EXPIRES
    )
    response_body = {
        "status": "success",
        "message": "user is logged out",
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('/forgot-password', methods=['GET'])
@jwt_refresh_token_required
def forgot_password():
    # TODO need to decode the @ sign for the email param
    # TODO send an email with temp 6 digit code
    # TODO store temp code under a redis hash forgot_password with key = email; need to escape the @ sign
    pass


@blueprint.route('/reset-password', methods=['PUT'])
@requires_json_content
def reset_password():
    # TODO will need to check redis for temp code
    pass


@blueprint.route('<int:user_id>/handicaps', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
def handicap(user_id):
    if request.method == 'GET':
        start_date = request.args.get('start')
        if start_date:
            handicaps = Handicap.get_by_date(user_id=user_id, start_date=start_date)
            results = handicap_schema.dump(handicaps, many=True)
            response_body = {
                'status': 'success',
                'result': results,
            }
            return make_response(jsonify(response_body), HTTPStatus.OK.value)
        else:
            current_handicap = Handicap.get_active(user_id=user_id)
            result = handicap_schema.dump(current_handicap)
            response_body = {
                'status': 'success',
                'result': result,
            }
            return make_response(jsonify(response_body), HTTPStatus.OK.value)

    current_handicap = Handicap.get_active(user_id=user_id)
    current_handicap.close()
    request_body = request.get_json()
    request_body['user_id'] = user_id
    try:
        data = handicap_schema.load(request_body)
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    new_handicap = Handicap(**data)
    new_handicap.save()
    response_body = {
        'status': 'success',
        'message': f"Handicap was successfully added for user_id: '{user_id}'",
        'uri': f'/user/{user_id}/handicaps',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('<int:user_id>/golf-rounds', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
def golf_rounds(user_id):
    if request.method == 'GET':
        rounds = GolfRound.get_by_user_id(user_id=user_id)
        results = golf_round_schema.dump(rounds, many=True)
        response_body = {
            'status': 'success',
            'result': results.data,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    request_body = request.get_json()
    request_body['user_id'] = user_id
    try:
        golf_round = golf_round_schema.load(request_body)
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    new_round = GolfRound(**golf_round.data)
    golf_round_id = new_round.save()
    response_body = {
        'status': 'success',
        'message': f"GolfRound: '{golf_round_id}' was successfully added for user_id: '{user_id}'",
        'uri': f'/user/{user_id}/golf-rounds/{golf_round_id}',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)


@blueprint.route('<int:user_id>/golf-rounds/<int:golf_round_id>/golf-round-stats', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
def golf_round_stats(user_id, golf_round_id):
    if request.method == 'GET':
        round_stats = GolfRoundStats.get_by_golf_round_id(golf_round_id=golf_round_id)
        results = golf_round_stats_schema.dump(round_stats, many=True)
        response_body = {
            'status': 'success',
            'result': results,
        }
        return make_response(jsonify(response_body), HTTPStatus.OK.value)

    request_body = request.get_json()
    if not request_body.get('round_stats'):
        response_body = {
            'status': 'fail',
            'message': "Request is missing required parameter: 'round_stats'"
        }
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    round_stats_data = []
    for hole_stat in request_body.get('round_stats'):
        hole_stat['golf_round_id'] = golf_round_id
        try:
            data = golf_round_stats_schema.load(hole_stat)
        except ValidationError as e:
            response_body = {
                'status': 'fail',
                'message': e.messages
            }
            return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

        round_stats_data.append(GolfRoundStats(**data))

    GolfRoundStats.bulk_save(round_stats=round_stats_data)
    message = f"GolfRoundStats records were successfully added for GolfRound id: '{golf_round_id}'"
    response_body = {
        'status': 'success',
        'message': message,
        'uri': f'/users/{user_id}/golf-rounds/{golf_round_id}/golf-round-stats',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)
