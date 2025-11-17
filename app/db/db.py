from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.models.base import Base

engine = create_async_engine(settings.database_url, connect_args={"ssl": None})
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
	
	db = SessionLocal()
	try:
		yield db
	finally:
		await db.close()