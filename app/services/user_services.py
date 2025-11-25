from http import HTTPStatus

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from wtforms.validators import Email
from app.auth.password_utils import hash_password

from app.models.user_model import User


async def check_email(email: EmailStr, db: AsyncSession):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user_info = result.scalar_one_or_none()
    if user_info:
        return True
    return False

async def user_create(name: str, password: str, email: EmailStr, db: AsyncSession):
    if await check_email(email, db):
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )
    hashed_password = hash_password(password)
    new_user = User(password=hashed_password, name=name, email=email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def user_read(user_id: int, db: AsyncSession):
    query = select(User).filter_by(id = user_id)
    result = await db.execute(query)
    user_info = result.scalar_one_or_none()
    if not user_info:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user_info


async def user_read_by_username(username: str, db: AsyncSession):
    query = select(User).filter_by(name = username)
    result = await db.execute(query)
    user_info = result.scalar_one_or_none()
    return user_info


async def read_all_users(db: AsyncSession):
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


async def user_update(user_id: int, db: AsyncSession, new_name: str | None = None, new_email: EmailStr | None = None):
    user_to_update = await user_read(user_id, db)
    if new_name is not None:
        user_to_update.name = new_name
    if new_email is not None:
        if await check_email(new_email, db):
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            )
        else:
            user_to_update.email = new_email
    if new_email is None and new_name is None:
        raise HTTPException(status_code=400, detail="You need to specify at least one field")
    await db.commit()
    await db.refresh(user_to_update)
    return user_to_update


async def user_delete(user_id: int, db: AsyncSession):
    user = await user_read(user_id, db)
    await db.delete(user)
    await db.commit()
    return {'msg': 'User deleted'}