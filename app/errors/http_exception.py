from datetime import datetime

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    time = datetime.now()
    timestamp = time.timestamp()
    return JSONResponse({"errors": [exc.detail], "timestamp": timestamp}, status_code=exc.status_code)

