import logging
import os
import socket
import sys
from io import BytesIO
from typing import Any
from urllib import parse

from http_framework import HttpFramework
from wsgi.hot_reload import HotReload

logger = logging.getLogger(__name__)


class WSGIServer:
    """
    WSGI Server
    """

    def __init__(
        self,
        app: HttpFramework,
        host: str = "127.0.0.1",
        port: int = 8000,
        hot: bool = True,
        hot_dir: str = ".",
    ) -> None:
        self.app = app
        self.host = host
        self.port = port

        if hot:
            self.reloader = HotReload(callback=self.restart_server, directory=hot_dir)
            self.reloader.start()

    def serve_forever(self) -> None:
        """
        Starts the server

        Raises:
            OSError: If the server fails to start.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            logger.info(f"WSGIServer: Serving HTTP on {self.host} port {self.port} ...")

            while True:
                client_connection, client_address = server_socket.accept()
                self.handle_request(client_connection)
                client_connection.close()

    def handle_request(self, client_connection: socket.socket) -> None:
        """
        Handles a single HTTP request

        Parameters:
            client_connection (socket.socket): The client connection.

        Raises:
            OSError: If the server fails to handle the request.
        """

        request_data = client_connection.recv(65536)
        request_text = request_data.decode("utf-8")
        env = self.get_environ(request_text)

        response = BytesIO()

        def start_response(
            status: str, headers: list[tuple[str, str]], _: Any = None
        ) -> None:
            """
            Start the response

            Parameters:
                status (str): The status of the response.
                headers (list[tuple[str, str]]): The headers of the response.
                _: Any: Unused.

            Raises:
                OSError: If the server fails to start the response.
            """
            response_headers = [f"HTTP/1.1 {status}"] + [
                f"{header[0]}: {header[1]}" for header in headers
            ]
            response.write("\r\n".join(response_headers).encode("utf-8") + b"\r\n\r\n")

        result = self.app(env, start_response)

        for data in result:
            response.write(data)
        response_bytes = response.getvalue()
        client_connection.sendall(response_bytes)

    @staticmethod
    def get_environ(request_text: str) -> dict:
        """
        Gets the environ from the request text

        Parameters:
            request_text (str): The request text.

        Returns:
            dict: The environ.
        """

        request_line, headers_alone = request_text.split("\r\n", 1)
        headers, body = headers_alone.split("\r\n\r\n", 1)

        method, path, _ = request_line.split(" ")
        headers = headers.split("\r\n")

        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": parse.unquote(path),
            "QUERY_STRING": parse.urlparse(path).query,
            "CONTENT_TYPE": "text/plain",
            "CONTENT_LENGTH": str(len(body)),
            "wsgi.version": (1, 0),
            "wsgi.url_scheme": "http",
            "wsgi.input": BytesIO(body.encode("utf-8")),
            "wsgi.errors": BytesIO(),
            "wsgi.multithread": False,
            "wsgi.multiprocess": True,
            "wsgi.run_once": False,
        }

        # Parse headers
        for header in headers:
            name, value = header.split(": ", 1)
            name = name.upper().replace("-", "_")
            if name == "CONTENT_TYPE":
                environ["CONTENT_TYPE"] = value
            elif name == "CONTENT_LENGTH":
                environ["CONTENT_LENGTH"] = value
            else:
                environ[f"HTTP_{name}"] = value

        return environ

    @staticmethod
    def restart_server() -> None:
        """Restarts the current process with the same arguments."""

        os.execv(sys.executable, ["python"] + sys.argv)
