import json
from io import BytesIO
from typing import TYPE_CHECKING

from http_framework import Response

if TYPE_CHECKING:
    from http_framework import HttpFramework


class TestClient:
    def __init__(self, framework: "HttpFramework"):
        self.framework = framework

    def simulate_request(
        self, path: str, method: str = "GET", data: dict = None, headers: list = None
    ) -> Response:
        if data is None:
            data = {}
        if headers is None:
            headers = []

        data_bytes = json.dumps(data).encode("utf-8")
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "CONTENT_TYPE": "application/json",
            "CONTENT_LENGTH": str(len(data_bytes)),
            "wsgi.input": BytesIO(data_bytes),
            "wsgi.errors": BytesIO(),
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.run_once": True,
            "wsgi.multithread": False,
            "wsgi.multiprocess": False,
            "HTTP_HOST": "testserver",
            "SERVER_NAME": "testserver",
            "SERVER_PORT": "80",
        }

        for name, value in headers:
            environ["HTTP_" + name.upper().replace("-", "_")] = value

        start_response_status = 200
        start_response_headers = []

        def start_response(status, response_headers, exc_info=None):
            start_response_status = status
            start_response_headers = response_headers

        # Simulate a request
        response_body = self.framework(environ, start_response)
        response = Response(
            status=start_response_status,
            headers=start_response_headers,
            body=b"".join(response_body),
        )

        return response

    def get(self, path: str, **kwargs):
        return self.simulate_request(path, "GET", **kwargs)

    def post(self, path: str, data: dict, **kwargs):
        return self.simulate_request(path, "POST", data=data, **kwargs)
