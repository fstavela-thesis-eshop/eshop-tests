from typing import Any

from requests import Response
from requests import Session


class APIClient:
    def __init__(
        self, username: str, password: str, base_url: str = "http://localhost:8080"
    ):
        self.base_url = base_url
        self.session = Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.headers.update({"Accept": "application/json"})
        self.session.auth = (username, password)

    def request(
        self, method: str, endpoint: str, *args: Any, **kwargs: Any
    ) -> Response:
        return self.session.request(method, self.base_url + endpoint, *args, **kwargs)

    def get(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("GET", endpoint, *args, **kwargs)

    def post(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("POST", endpoint, *args, **kwargs)

    def put(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("PUT", endpoint, *args, **kwargs)

    def delete(self, endpoint: str, *args: Any, **kwargs: Any) -> Response:
        return self.request("DELETE", endpoint, *args, **kwargs)
