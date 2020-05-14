from http import HTTPStatus

from flask import (
    Blueprint,
    jsonify,
    make_response,
    request
)

from api.helpers import (
    throws_500_on_exception,
)
from api import search


blueprint = Blueprint('search', __name__)


@blueprint.route('/<index>', methods=['GET'])
@throws_500_on_exception
def search_index(index):
    search_text = request.args.get('q')
    search_results = search.full_text_search(
        index=index,
        field='name',
        text=search_text
    )
    hits = search_results['hits']['hits']

    response_body = {'results': hits}
    return make_response(jsonify(response_body), HTTPStatus.OK.value)
