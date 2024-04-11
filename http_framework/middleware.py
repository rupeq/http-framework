import abc

from http_framework.request import Request
from http_framework.response import Response


class Middleware(abc.ABC):
    """
    Middleware class
    """

    @abc.abstractmethod
    def process_request(self, request: Request) -> Request:
        """
        Process request

        Parameters:
            request (Request): request

        Returns:
            Request: request
        """
        raise NotImplementedError

    @abc.abstractmethod
    def process_response(self, request: Request, response: Response) -> Response:
        """
        Process response

        Parameters:
            request (Request): request
            response (Response): response

        Returns:
            Response: response
        """
        raise NotImplementedError
