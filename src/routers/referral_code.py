from fastapi import APIRouter, Depends
from pydantic import EmailStr
from src.models.referral_code import ReferralCode
from src.models.user import User
from src.repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import get_async_session
from src.auth.dependencies import get_current_user
from src.schemas.user import UserOut
from src.utils.utils import generate_new_referral_code
from exceptions import ReferralCodeNotFound, UserNotFound
from fastapi.responses import JSONResponse
from src.repositories.referrals_code import ReferralCodeRepository
from datetime import datetime, timezone
from src.schemas.referral_code import ReferralCodeSchema


referral_code_router: APIRouter = APIRouter(
    prefix='/referral_code',
    tags=['Реферальный код']
)



@referral_code_router.post('')
async def create_new_referral_code(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[UserOut, Depends(get_current_user)]
) -> str | None:
    if user:
        ref_code: ReferralCode = await ReferralCodeRepository.find_one_or_none(session=session, user_id=user.id)
        today = datetime.now(timezone.utc)
        new_referral_code: str = generate_new_referral_code()
        referral_code: ReferralCodeSchema = ReferralCodeSchema(user_id=user.id, referral_code=new_referral_code)
        if not ref_code:
            await ReferralCodeRepository.add(session=session, **referral_code.model_dump())
            return new_referral_code

        if today > ref_code.expiration_date:
            await ReferralCodeRepository.delete(session=session, id=ref_code.id)
            await ReferralCodeRepository.add(session=session, **referral_code.model_dump())
            return new_referral_code

        return JSONResponse(
            content={
                'error': 'Прошлый код еще действует, чтобы создать новый - удалите старый, или дождитесь когда истечет срок'
            },
            status_code=400
        )


@referral_code_router.delete('')
async def delete_referral_code(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user: Annotated[UserOut, Depends(get_current_user)]
) -> str | None:
    ref_code: ReferralCode = await ReferralCodeRepository.find_one_or_none(session=session, user_id=user.id)
    if not ref_code or ref_code.user_id != user.id:
        raise ReferralCodeNotFound
    await ReferralCodeRepository.delete(session=session, id=ref_code.id)
    return JSONResponse(
        content={'success': 'Referral Code deleted'},
        status_code=200
    )




@referral_code_router.get('')
async def get_my_referral_code(
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> str | None:
    ref_code: ReferralCode = await ReferralCodeRepository.find_one_or_none(session=session, user_id=user.id)
    if ref_code:
        return ref_code.referral_code
    return None



@referral_code_router.get('/get/{email}')
async def get_referral_code_by_email(
    email: EmailStr,
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    user: User = await UserRepository.find_one_or_none(session=session, email=email)
    if user:
        if user.referral_codes:
            return JSONResponse(
                content={'Referral Code': user.referral_codes.referral_code},
                status_code=200
            )
        else:
            raise ReferralCodeNotFound
    else:
        raise UserNotFound
