from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer

from app.auth import auth_utils,jwt_utils
from app.schemas.token_schema import TokenSchema
from app.schemas.user_schemas import UserSchema

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/login",
    tags=["login"],
    dependencies=[Depends(http_bearer)],
)


@router.post("/", response_model=TokenSchema)
async def login(response: Response,user: UserSchema = Depends(auth_utils.validate_auth_user)):
    access_token = await jwt_utils.create_access_token(user)
    refresh_token = await jwt_utils.create_refresh_token(user)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='lax',
        path='/'
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/refresh", response_model=TokenSchema)
async def issue_new_access_token(
        response: Response,
        user: UserSchema = Depends(auth_utils.get_current_user_for_refresh)
):
    access_token = await jwt_utils.create_access_token(user)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        samesite='lax',
        path='/'
    )
    return {
        "access_token": access_token,
    }