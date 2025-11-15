from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn
import redis
from redis import Redis
import httpx
import json

from app.core.config import settings
from app.models.product import Product

from contextlib import asynccontextmanager

from app.db.db import get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
	app.state.redis = Redis(host=settings.app_host, port=6379)
	app.state.http_client = httpx.AsyncClient()
	yield
	app.state.redis.close()

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def root():
	return {"msg": settings}


@app.get('/entries')
async def read_item():
	# value = app.state.redis.get('entries')
	# if value is None:
	# 	value = 'qwe'
	# 	app.state.redis.set('entries', value)
	# 	return {"msg": 'redis didnt do anything'}
	# else:
	# 	return {'msg': 'redis did it job', 'redis_response': value}
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


@app.post('/qwe')
async def index(name: str, price: int, description: str, db: AsyncSession = Depends(get_db)):
	db_user = Product(name=name, price=price, description=description)
	db.add(db_user)
	await db.commit()
	await db.refresh(db_user)
	return db_user



if __name__ == '__main__':
	uvicorn.run(app, host="0.0.0.0", port=8000)