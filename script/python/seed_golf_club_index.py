import requests
import json
from typing import List
from http import HTTPStatus

from api.schemas import GolfClubSchema, GolfCourseSchema
from api.repositories.golf_club_repository import golf_club_repo
from api.repositories.golf_course_repository import golf_course_repo

GOLF_CLUB_INDEX_NAME = 'golf_club'
ES_API_URL_BASE = 'http://0.0.0.0:8001/'

golf_club_schema = GolfClubSchema()
golf_course_schema = GolfCourseSchema()


def index_exists(index: str) -> bool:
    url = f"{ES_API_URL_BASE}{index}"
    res = requests.head(url)
    if res.status_code == HTTPStatus.OK:
        return True
    elif res.status_code == HTTPStatus.NOT_FOUND:
        return False


def create_index(index: str, nested_properties: List[str]):
    properties_dict = {nested_property: {"type": "nested"} for nested_property in nested_properties}
    if not index_exists(index=index):
        url = f"{ES_API_URL_BASE}{GOLF_CLUB_INDEX_NAME}"
        body = {
            "mappings": {
                "properties": properties_dict
            }
        }
        headers = {"Content-Type": "application/json"}
        res = requests.put(
            url=url,
            data=json.dumps(body),
            headers=headers
        )
        if not res.ok:
            print(res.text)
            raise Exception(f"Failed to create the index: {index}")


def build_request_bodies() -> List[dict]:
    request_bodies = []
    golf_clubs_records = golf_club_repo.get_all()
    for golf_club in golf_clubs_records:
        golf_course_records = golf_course_repo.get_by_golf_club_id(golf_club_id=golf_club.id)
        golf_course_data = golf_course_schema.dump(golf_course_records, many=True).data
        golf_club_data = golf_club_schema.dump(golf_club).data
        golf_club_data['golf_courses'] = golf_course_data
        request_body = {
            "payload": golf_course_data,
            "_id": golf_club_data["id"],
        }
        request_bodies.append(request_body)

    golf_course_repo.db_session.remove()
    golf_club_repo.db_session.remove()
    return request_bodies


def create_documents(target_index: str, request_bodies: List[dict]):
    url = f"{ES_API_URL_BASE}{target_index}/_doc"
    headers = {"Content-Type": "application/json"}
    for request_body in request_bodies:
        res = requests.post(
            url=url,
            data=json.dumps(request_body, default=str),
            headers=headers
        )


def seed():
    nested_properties = ["golf_courses"]
    create_index(
        index=GOLF_CLUB_INDEX_NAME,
        nested_properties=nested_properties
    )
    request_bodies = build_request_bodies()
    create_documents(
        target_index=GOLF_CLUB_INDEX_NAME,
        request_bodies=request_bodies
    )


if __name__ == "__main__":
    seed()
