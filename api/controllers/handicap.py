from flask import (
    Blueprint,
    request,
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from api.services import handicap_service
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
    service = handicap_service.HandicapService(
        repo=handicap_repo,
        schema=handicap_schema,
    )
    if request.method == 'GET':
        start_date = request.args.get('start')
        if start_date:
            return service.get_by_date(user_id=user_id, date=start_date)

        return service.get_active(user_id=user_id)

    payload = request.get_json()
    return service.add(user_id=user_id, payload=payload)
