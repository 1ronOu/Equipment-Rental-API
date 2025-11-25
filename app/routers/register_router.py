from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
from app.schemas.user_schemas import UserCreate
from app.services import user_services

router = APIRouter(
    prefix="/register",
    tags=["register"],
)


@router.post('/')
async def register_new_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await user_services.user_create(
        name=user.name,
        email=user.email,
        password=user.password,
        db=db
    )
    return new_user