from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_utils import get_current_user
from app.db.db import get_db
from app.schemas.user_schemas import UserSchema


async def require_admin(user: UserSchema = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if user.role == 'admin':
        return user
    else:
        raise HTTPException(
            status_code=403,
            detail='You do not have permission to perform this action.'
        )