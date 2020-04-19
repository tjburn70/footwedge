from http import HTTPStatus

from flask import Blueprint, jsonify, make_response

blueprint = Blueprint('health', __name__)


@blueprint.route('/')
def healthcheck():
    return make_response(jsonify({'status': 'pass'}), HTTPStatus.OK.value)
