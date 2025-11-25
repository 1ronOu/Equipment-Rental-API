from jwt import InvalidTokenError

from fastapi import Form, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_utils import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from app.db.db import get_db
from app.services import user_services
from app.auth import password_utils, jwt_utils

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        db: AsyncSession = Depends(get_db)
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password',
    )
    user = await user_services.user_read_by_username(username=username, db=db)
    if not user:
        raise unauthed_exc

    if not password_utils.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc

    return user


async def get_current_user_payload(request: Request):
    try:
        token = request.cookies.get('access_token')
        payload = jwt_utils.decode_jwt(token=token)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token error: {e}',
        )


async def validate_token_type(payload: dict, token_type: str):
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Invalid token type {current_token_type}',
        )


async def get_current_user(
        payload: dict = Depends(get_current_user_payload),
        db: AsyncSession = Depends(get_db)
):
    await validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    user_id = int(payload.get('sub'))
    user = await user_services.user_read(user_id=user_id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid password or username',
        )
    return user


async def get_current_user_for_refresh(
        payload: dict = Depends(get_current_user_payload),
        db: AsyncSession = Depends(get_db)
):
    await validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    user_id = int(payload.get('sub'))
    user = await user_services.user_read(user_id=user_id, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid password or username',
        )
    return user

