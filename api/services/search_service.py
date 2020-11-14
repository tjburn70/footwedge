import os
import logging

import requests

API_BASE_URL = os.environ.get('SEARCH_SERVICE_API_BASE_URL')
GOLF_CLUB_INDEX = "golf_club"
GOLF_COURSE_NESTED_PROPERTY = "golf_courses"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchService:
    """ A client for the search service to ensure RDBS kept in-sync with ElasticSearch"""

    @staticmethod
    def add_golf_club(golf_club_id: int, payload: dict):
        url = f"{API_BASE_URL}/{GOLF_CLUB_INDEX}/_doc"
        body = {
            "payload": payload,
            "_id": golf_club_id,
        }
        resp = requests.put(
            url=url,
            json=body
        )
        if not resp.ok:
            logger.info(
                f"Uh oh something went wrong when saving golf_club: {golf_club_id} to search service... \n"
                f"Resp: {resp.text}"
            )

    @staticmethod
    def add_golf_course(golf_club_id: int, payload: dict):
        url = f"{API_BASE_URL}/{GOLF_CLUB_INDEX}/_doc/{golf_club_id}/_update/{GOLF_COURSE_NESTED_PROPERTY}"
        resp = requests.put(
            url=url,
            json=payload
        )
        if not resp.ok:
            logger.info(
                f"Issue when saving golf_course to golf_club: {golf_club_id} to search service... \n"
                f"Resp: {resp.text}"
            )
