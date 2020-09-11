import requests

AUTH_SERVICE_TOKEN_URL = ""
FOOTWEDGE_API_URL = "http://localhost:8000/api"


# TODO: implement integration with auth service
def get_access_token() -> str:
    return "token"


class FootwedgeApi:

    def __init__(self):
        self.access_token = get_access_token()

    def build_headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    def call(self, method: str, path: str, **kwargs):
        """
        http request
        """
        url = f"{FOOTWEDGE_API_URL}{path}"
        resp = requests.request(
            method=method,
            url=url,
            headers=self.build_headers(),
            timeout=10.0,
            verify=False,
            **kwargs
        )

        return resp
