from logging import Logger
from typing import Callable, Awaitable

from fastapi import Request, Response


class LoggingMiddleware:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    async def __call__(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get("X-Request-Id")

        self.logger.info(f"Received request with ID {request_id}")
        response = await call_next(request)
        self.logger.info(f"Request with ID {request_id} processed successfully")

        return response
