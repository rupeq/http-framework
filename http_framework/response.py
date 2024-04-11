import json
from typing import Any, Callable


class Response:
    """
    Response class
    """

    def __init__(
        self,
        body: str | bytes = "",
        status: int = 200,
        headers: list[tuple[str, str]] | None = None,
        content_type: str = "text/plain",
    ) -> None:
        self.body = body if isinstance(body, bytes) else str(body).encode("utf-8")
        self.status = status
        self.headers = headers if headers is not None else []

        if (
            headers is None
            or not any(
                [header for header in headers if header[0].lower() == "content-type"]
            )
            and content_type
        ):
            self.headers.append(("Content-Type", content_type))

        self._status_messages = {
            200: "OK",
            301: "Moved Permanently",
            404: "Not Found",
            500: "Internal Server Error",
        }

    @property
    def json(self):
        try:
            return json.loads(self.body)
        except json.JSONDecodeError:
            return {}

    def set_header(self, name: str, value: str) -> None:
        """
        Set header

        Parameters:
            name (str): header name
            value (str): header value
        """

        self.headers.append((name, value))

    def set_cookie(self, key: str, value: str, **kwargs: Any) -> None:
        """
        Set cookie

        Parameters:
            key (str): cookie name
            value (str): cookie value

        Kwargs:
            kwargs (Any): additional headers
        """

        cookie = f"{key}={value}"
        for k, v in kwargs.items():
            cookie += f"; {k}={v}"
        self.set_header("Set-Cookie", cookie)

    def get_status(self) -> str:
        """
        Get status

        Returns:
            str: status
        """

        return f"{self.status} {self._status_messages.get(self.status, 'Unknown')}"

    def get_response(self, start_response: Callable) -> None:
        """
        Get response

        Parameters:
            start_response (Callable): start_response
        """

        start_response(self, self.headers)
