import os
import requests

API_BASE_URL = os.environ.get('SEARCH_SERVICE_API_BASE_URL')
GOLF_CLUB_INDEX = "golf_club"
GOLF_COURSE_NESTED_PROPERTY = "golf_courses"


class SearchService:
    """ A client for the search service to ensure RDBS kept in-sync with ElasticSearch"""

    @staticmethod
    def add_golf_club(golf_club_id: int, payload: dict):
        url = f"{API_BASE_URL}/{GOLF_CLUB_INDEX}/_doc"
        body = {
            "payload": payload,
            "_id": golf_club_id,
        }
        requests.put(
            url=url,
            json=body
        )

    @staticmethod
    def add_golf_course(golf_club_id: int, payload: dict):
        url = f"{API_BASE_URL}/{GOLF_CLUB_INDEX}/_doc/{golf_club_id}/_update/{GOLF_COURSE_NESTED_PROPERTY}"
        requests.put(
            url=url,
            json=payload
        )
