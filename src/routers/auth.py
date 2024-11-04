from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from exceptions import UserAlreadyExistsException, UserNotFound
from src.auth.auth import authenticate_user, create_access_token, get_password_hash
from src.auth.dependencies import get_current_user
from src.models.referral_code import ReferralCode
from src.models.user import User
from src.repositories.user import UserRepository
from src.schemas.user import UserRegister, UserOut, UserLogin
from src.repositories.referrals_code import ReferralCodeRepository
from src.repositories.referrals import ReferralsRepository
from src.schemas.referral import ReferralSchema
from exceptions import ReferralCodeNotFound, ReferralCodeExpiredException



auth_router: APIRouter = APIRouter(
    prefix='/auth', tags=['Аутентификация и Авторизация']
)



@auth_router.post('/register', status_code=201)
async def rigister_user(
    user: UserRegister,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserOut:

    exist_user: UserOut = await UserRepository.find_one_or_none(
        session=session, email=user.email
    )

    if exist_user:
        raise UserAlreadyExistsException
    current_date_time: datetime = datetime.now(timezone.utc)
    hashed_password: str = get_password_hash(user.password)
    
    referred_by: int | None = None

    if user.referral_code:
        ref_code: ReferralCode = await ReferralCodeRepository.find_one_or_none(session=session, referral_code=user.referral_code)
        if ref_code:
            referred_by = ref_code.user_id
            if current_date_time > ref_code.expiration_date:
                raise ReferralCodeExpiredException
        else:
            raise ReferralCodeNotFound

    new_user: User = await UserRepository.add(
        session=session, 
        email=user.email, 
        hashed_password=hashed_password, 
        registered_at=current_date_time, 
        referred_by=referred_by)

    if referred_by:
        new_referral: ReferralSchema = ReferralSchema(user_id=new_user.id, referred_by=referred_by)
        await ReferralsRepository.add(session=session, **new_referral.model_dump())

    new_user_out: UserOut = UserOut.model_validate(new_user)
    return new_user_out



@auth_router.post("/login", status_code=200)
async def login_user(
    response: Response,
    user: UserLogin,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str:

    user: UserOut = await authenticate_user(user.email, user.password, async_db=session)
    if not user:
        raise UserNotFound

    access_token = create_access_token({'sub': str(user.id)})

    response.set_cookie(
        'user_access_token', access_token, httponly=True
    )
    return access_token




@auth_router.post('/logout', status_code=200)
async def logout_user(
    response: Response,
    request: Request,
):
    cookies: str | None = request.cookies.get('user_access_token')
    if cookies:
        response.delete_cookie(key='user_access_token')