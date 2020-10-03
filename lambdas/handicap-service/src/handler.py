import json

from lib.footwedge_api import FootwedgeApi
from lib.service import HandicapService


def lambda_handler(event, context):
    print(json.dumps(event))
    for record in event['Records']:
        payload = json.loads(record["body"])
        user_id = payload.get("user_id")
        HandicapService(
            footwedge_api_client=FootwedgeApi(),
            user_id=user_id,
        ).post_handicap()
