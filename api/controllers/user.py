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
)

from api.config import REFRESH_EXPIRES
from api.controllers import auth
from api.schemas import (
    HandicapSchema,
    GolfRoundSchema,
    GolfRoundStatsSchema
)
from api.helpers import (
    requires_json_content,
    throws_500_on_exception,
)
from api.repositories.user_repository import user_repo


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

    if user_repo.get_by_email(email):
        error_message = f"A user with email: '{email}' already exists!"
        response_body = {"message": error_message}
        return make_response(jsonify(response_body), HTTPStatus.BAD_REQUEST.value)

    new_user = user_repo.create(data=request_body)
    user_id = new_user.id
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

    current_user = user_repo.get_by_email(email=email)
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
