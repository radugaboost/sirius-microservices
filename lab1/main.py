from fastapi import FastAPI, Response, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from starlette.status import HTTP_400_BAD_REQUEST

from schemas.request import DoRequest
from utils.logger import setup_logger
from middleware.logging import LoggingMiddleware

from config.jobs import JOB_TO_FUNCTION
from config.settings import DefaultSettings
from middleware.metrics import MetricsMiddleware
from schemas.response import DefaultResponse

settings = DefaultSettings()
logger = setup_logger(settings.SERVICE_NAME)

app = FastAPI()

app.middleware("http")(MetricsMiddleware())
app.middleware("http")(LoggingMiddleware(logger))


@app.post("/api/v1/do", response_model=DefaultResponse)
async def do(body: DoRequest) -> dict[str, float]:
    func = JOB_TO_FUNCTION[settings.DO_JOB]

    try:
        result = func(body.number)
    except ValueError as err:
        logger.error(err)
        raise HTTPException(detail=str(err), status_code=HTTP_400_BAD_REQUEST)

    return {"result": result}


@app.get("/metrics")
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
