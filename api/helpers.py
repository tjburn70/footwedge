import sys
import logging
from http import HTTPStatus
from functools import wraps

from flask import request, make_response, jsonify

logger = logging.getLogger(__name__)


def requires_json_content(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return make_response(
                "Expecting Content-Type: application/json or compatible",
                HTTPStatus.BAD_REQUEST.value
            )
        else:
            return f(*args, **kwargs)

    return decorated


def throws_500_on_exception(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            response = f(*args, **kwargs)
        except Exception:
            exception_type, exception, exception_traceback = sys.exc_info()
            details = f"An exception occurred processing request. {exception_type}: {exception}, {exception_traceback}"
            logger.error(details)
            response_body = {
                "message": "Apologies, an exception occurred",
                "details": details,
            }
            response = make_response(jsonify(response_body), 500)

        return response

    return decorated
