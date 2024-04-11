import logging

from http_framework import Middleware, Request, Response

logger = logging.getLogger(__name__)


class MiddlewareExample(Middleware):
    def process_request(self, request: Request) -> Request:
        logger.info("Received request: %s", request)
        return request

    def process_response(self, request: Request, response: Response) -> Response:
        logger.info("Sending response: %s", response)
        return response
