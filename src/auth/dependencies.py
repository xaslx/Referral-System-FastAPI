from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config import env_config
from database import get_async_session
from exceptions import IncorrectTokenException, TokenAbsentException, UserIsNotPresentException, TokenExpiredException, UserNotFound
from src.models.user import User
from src.repositories.user import UserRepository
from src.models.user import User
from src.schemas.user import UserOut


def get_token(request: Request):
    token: str = request.cookies.get('user_access_token')
    if not token:
        return None
    return token


def valid_token(token: str):
    try:
        payload = jwt.decode(token, env_config.SECRET_KEY, env_config.SECRET_ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenException
    return payload


async def get_current_user(
    async_db: AsyncSession = Depends(get_async_session),
    token: str = Depends(get_token),
) -> UserOut:
    if token:
        payload = valid_token(token=token)
        user_id: str = payload.get('sub')
        user: User = await UserRepository.find_one_or_none(
            id=int(user_id), session=async_db
        )
        if not user_id:
            raise UserIsNotPresentException
        if not user:
            raise UserNotFound
        user: UserOut = UserOut.model_validate(user)
        return user
    else:
        raise TokenAbsentException