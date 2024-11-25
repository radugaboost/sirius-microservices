from uuid import uuid4

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from starlette.status import HTTP_400_BAD_REQUEST

from config.settings import RpcSettings
from utils.logger import setup_logger

app = FastAPI()

settings = RpcSettings()
logger = setup_logger(settings.SERVICE_NAME)


METHOD_TO_SERVER = {
    "to_square": settings.TO_SQUARE_URL,
    "to_sqrt": settings.TO_SQRT_URL,
}


@app.post("/rpc")
async def handle_rpc(request: Request) -> JSONResponse:
    logger.info("Received RPC request")
    rpc_request = await request.json()
    method = rpc_request.get("method")
    data = rpc_request.get("data")
    request_id = rpc_request.get("requestId", uuid4())

    url = METHOD_TO_SERVER.get(method)
    if not url:
        raise HTTPException(detail={"error": "Unknown method"}, status_code=HTTP_400_BAD_REQUEST)

    async with AsyncClient() as client:
        response = await client.post(url, json=data, headers={"X-Request-Id": str(request_id)})

    return JSONResponse(content=response.json(), status_code=response.status_code)