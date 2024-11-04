from fastapi import APIRouter, Depends
from src.models.referrals import Referral
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from database import get_async_session
from src.auth.dependencies import get_current_user
from src.repositories.referrals import ReferralsRepository
from src.schemas.user import UserOut
from src.schemas.referral import ReferralOutSchema


referrals_router: APIRouter = APIRouter(
    prefix='/referrals',
    tags=['Рефералы']
)



@referrals_router.get('')
async def get_my_referrals(
    user: Annotated[UserOut, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> list[ReferralOutSchema]:
    all_referrals: list[Referral] = await ReferralsRepository.find_all(session=session, referred_by=user.id)
    referral_data: list[ReferralOutSchema] = [ReferralOutSchema.model_validate(ref) for ref in all_referrals]
    
    return referral_data