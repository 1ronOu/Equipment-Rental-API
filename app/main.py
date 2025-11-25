import time
import logging

from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException

import uvicorn
from redis import Redis
import httpx
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.routers.user_router import router as user_router
from app.routers.equipment_router import router as equipment_router
from app.routers.login_router import router as login_router
from app.routers.register_router import router as register_router
from app.errors.http_exception import http_error_handler

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
	app.state.redis = Redis(host=settings.app_host, port=6379)
	app.state.http_client = httpx.AsyncClient()
	yield
	app.state.redis.close()


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
	start_time = time.time()
	response = await call_next(request)
	process_time = time.time() - start_time
	response.headers["X-Process-Time"] = str(process_time)
	return response


class LoggingMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, call_next):
		client_ip = request.client.host
		method = request.method
		url = request.url.path

		logger.info(f"Request: {method} {url} from {client_ip}")
		response = await call_next(request)
		status_code = response.status_code
		logger.info(f"Response: {method} {url} returned {status_code} to {client_ip}")

		return response

# Add middleware to the app
app.add_middleware(LoggingMiddleware)

app.add_exception_handler(HTTPException, http_error_handler)

app.include_router(user_router)
app.include_router(equipment_router)
app.include_router(login_router)
app.include_router(register_router)

@app.get('/')
async def root():
	return {"msg": settings}


if __name__ == '__main__':
	uvicorn.run(app, host="127.0.0.1", port=8000)