from time import time
from typing import Callable, Awaitable

from fastapi import Request, Response
from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter("app_requests_total", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])


class MetricsMiddleware:
    async def __call__(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time()

        REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()

        response = await call_next(request)

        request_latency = time() - start_time
        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(request_latency)

        return response