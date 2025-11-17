from typing import List

from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import UserCreate, UserRead
from app.services import user_services
from app.db.db import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_services.user_read(user_id=user_id, db=db)
    return user


@router.get("/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await user_services.read_all_users(db=db)
    return users


@router.post('/', response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await user_services.user_create(name=user.name, email=user.email, password=user.password, db=db)
    return new_user


@router.patch('/{user_id}', response_model=UserRead)
async def update_user(
        user_id: int,
        new_name: str | None = Query(default=None, max_length=30),
        new_email: EmailStr | None = Query(default=None, max_length=30),
        db: AsyncSession = Depends(get_db)
):
    updated_user = await user_services.user_update(user_id=user_id, new_name=new_name, new_email=new_email, db=db)
    return updated_user


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    deleted_user = await user_services.user_delete(user_id=user_id, db=db)
    return deleted_user