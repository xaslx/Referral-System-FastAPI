from datetime import datetime, timedelta

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.user import UserRepository
from config import env_config
from database import get_async_session
from exceptions import IncorrectEmailOrPasswordException
from src.models.user import User


pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + timedelta(days=15)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, env_config.SECRET_KEY, env_config.SECRET_ALGORITHM)

    return encode_jwt


async def authenticate_user(
    email: EmailStr,
    password: str,
    async_db: AsyncSession = Depends(get_async_session),
) -> User:

    user: User = await UserRepository.find_one_or_none(email=email, session=async_db)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectEmailOrPasswordException
    return user