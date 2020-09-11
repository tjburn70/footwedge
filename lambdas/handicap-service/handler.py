import json

from .footwedge_api import FootwedgeApi
from .handicap_service import HandicapService


def lambda_handler(event, context):
    print(json.dumps(event))
    footwedge_api_client = FootwedgeApi()
    for record in event['Records']:
        payload = record["body"]
        print(str(payload))
        user_id = payload.get("user_id")
        print(user_id)

        HandicapService(
            footwedge_api_client=footwedge_api_client,
            user_id=user_id,
        ).post_handicap()
