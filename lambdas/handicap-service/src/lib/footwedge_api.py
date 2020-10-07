import requests

AUTH_SERVICE_TOKEN_URL = ""
FOOTWEDGE_API_URL = "https://f9e29d0532f9.ngrok.io/api"


class FootwedgeApi:

    def __init__(self):
        self.access_token = self.get_access_token()

    @staticmethod
    def get_access_token() -> str:
        # TODO: implement integration with auth service
        return ""

    def apply_auth_header(self, headers: dict):
        auth_key = "Authorization"
        headers[auth_key] = self.access_token

    def call(self, method: str, path: str, **kwargs):
        """
        http request
        """
        url = f"{FOOTWEDGE_API_URL}{path}"
        headers = kwargs.pop('headers', {})
        # headers = kwargs.get('headers') or {}
        # apply auth header
        # self.apply_auth_header(headers=headers)
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            timeout=10.0,
            verify=False,
            **kwargs
        )

        return resp
