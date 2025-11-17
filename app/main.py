from fastapi import Depends, FastAPI, Query
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
import redis
from redis import Redis
import httpx
import json

from sqlalchemy.util.preloaded import engine_url

from app.core.config import settings
from app.routers.user_router import router as user_router
from app.routers.equipment_router import router as equipment_router

from contextlib import asynccontextmanager

from app.db.db import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
	app.state.redis = Redis(host=settings.app_host, port=6379)
	app.state.http_client = httpx.AsyncClient()
	yield
	app.state.redis.close()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(equipment_router)

@app.get('/')
async def root():
	return {"msg": settings}


@app.get('/entries')
async def read_item():
	r = Redis(host=settings.redis_host, port=settings.redis_port, db=0, username='qwe', password='qwe')
	try:
		info = r.info()
		print(info['redis_version'])
		response = r.ping()
		if response:
			print("Success")
		else:
			print("No success")
	except redis.exceptions.RedisError as e:
		print(f'error: {e}')


if __name__ == '__main__':
	uvicorn.run(app, host="0.0.0.0", port=8000)