from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()

@app.get('/')
async def root():
	return {"msg": "Ok"}