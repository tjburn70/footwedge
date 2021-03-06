import json

from mangum import Mangum

from api import app

PATH_PREFIX = "/search"
adapter = Mangum(app, enable_lifespan=False, api_gateway_base_path=PATH_PREFIX, log_level='info')


def lambda_handler(event, context):
    print(json.dumps(event))
    response = adapter.handler(event=event, context=context)
    print("Response: ", response)

    return response
