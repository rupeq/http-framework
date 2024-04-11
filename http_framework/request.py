import json
from typing import Any
from urllib.parse import parse_qs


class Request:
    """
    Request class
    """

    def __init__(self, environ: dict[str, Any]) -> None:
        self._environ = environ
        self.method = environ["REQUEST_METHOD"]
        self.path = environ["PATH_INFO"]
        self.query = parse_qs(environ.get("QUERY_STRING", ""))
        self.content_type = environ.get("CONTENT_TYPE", "")
        self.content_length = int(environ.get("CONTENT_LENGTH", 0))

    @property
    def body(self) -> None | bytes:
        """
        Get request body

        Returns:
            Request body
        """

        if not hasattr(self, "_body"):
            self._body = self._environ["wsgi.input"].read(self.content_length)

        return self._body

    @property
    def json(self) -> None | dict[str, Any]:
        """
        Get request json

        Returns:
            JSON data
        """

        if self.content_type != "application/json":
            return None

        if not hasattr(self, "_json"):
            try:
                self._json = json.loads(self.body)
            except json.JSONDecodeError:
                self._json = None

        return self._json

    @property
    def form(self) -> dict[str, Any] | None:
        """
        Get request form

        Returns:
            Form data
        """

        if self.content_type == "application/x-www-form-urlencoded":
            return parse_qs(self.body.decode("utf-8"))

        return None
