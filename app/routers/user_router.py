from typing import List

from attr.filters import exclude
from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPBearer
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.admin_tools import require_admin
from app.schemas.user_schemas import UserCreate, UserRead, UserSchema, UserUpdate
from app.services import user_services
from app.db.db import get_db
from app.auth import auth_utils

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=UserRead)
async def read_user(user: UserSchema = Depends(auth_utils.get_current_user)):
    return user


@router.get("/", response_model=List[UserRead])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await user_services.read_all_users(db=db)
    return users


@router.post('/', response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await user_services.user_create(name=user.name, email=user.email, password=user.password, db=db)
    return new_user


@router.patch('/me', response_model=UserRead)
async def update_user(
        fields_to_update: UserUpdate,
        user: UserSchema = Depends(auth_utils.get_current_user),
        db: AsyncSession = Depends(get_db)
):
    updated_user = await user_services.user_update(
        user_id=user.id,
        new_name=fields_to_update.name,
        new_email=fields_to_update.email,
        db=db
    )
    return updated_user


@router.delete('/{user_id}')
async def delete_user(user_id: int, user: UserSchema = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    deleted_user = await user_services.user_delete(user_id=user_id, db=db)
    return deleted_user