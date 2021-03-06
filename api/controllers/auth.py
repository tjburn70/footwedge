from http import HTTPStatus

import redis
from flask import (
    Blueprint,
    jsonify,
    make_response
)
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_refresh_token_required,
)

from api.settings import settings

BLACKLISTED_TOKEN_FLAG = '1'
ACTIVE_TOKEN_FLAG = '0'

redis_client = redis.StrictRedis.from_url(
    url=settings.REDIS_URI,
    decode_responses=True
)
blueprint = Blueprint('auth', __name__)
jwt = JWTManager()


# callback to check if JWT has been revoked; accepts decoded JWT python dict
@jwt.token_in_blacklist_loader
def token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    token_status = redis_client.get(jti)
    if not token_status:
        return True
    return token_status == BLACKLISTED_TOKEN_FLAG


@blueprint.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    response_body = {
        'access_token': access_token,
        'user_id': user_id,
    }
    return make_response(jsonify(response_body), HTTPStatus.CREATED.value)
