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

from api.schemas import HandicapSchema
from api.helpers import (
    requires_json_content,
    throws_500_on_exception,
)
from api.repositories.handicap_repository import handicap_repo


blueprint = Blueprint('handicap', __name__)
handicap_schema = HandicapSchema()


@blueprint.route('/', methods=['GET', 'POST'])
@requires_json_content
@jwt_required
@throws_500_on_exception
def handicap():
    user_id = get_jwt_identity()
    if request.method == 'GET':
        start_date = request.args.get('start')
        if start_date:
            handicaps = handicap_repo.get_by_date(user_id=user_id, start_date=start_date)
            results = handicap_schema.dump(handicaps, many=True)
            response_body = {
                'status': 'success',
                'result': results.data,
            }
            return make_response(jsonify(response_body), HTTPStatus.OK.value)
        else:
            current_handicap = handicap_repo.get_active(user_id=user_id)
            result = handicap_schema.dump(current_handicap)
            response_body = {
                'status': 'success',
                'result': result.data,
            }
            return make_response(jsonify(response_body), HTTPStatus.OK.value)

    current_handicap = handicap_repo.get_active(user_id=user_id)
    handicap_repo.close(current_handicap)
    request_body = request.get_json()
    request_body['user_id'] = user_id
    try:
        handicap_data = handicap_schema.load(request_body).data
    except ValidationError as e:
        response_body = {
            'status': 'fail',
            'message': e.messages
        }
        return make_response(jsonify(response_body), HTTPStatus.UNPROCESSABLE_ENTITY.value)

    handicap_repo.create(data=handicap_data)
    response_body = {
        'status': 'success',
        'message': f"Handicap was successfully added for user_id: '{user_id}'",
        'uri': f'/user/{user_id}/handicaps',
    }
    return make_response(jsonify(response_body), HTTPStatus.OK.value)
