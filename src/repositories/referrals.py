from src.models.referrals import Referral
from src.repositories.sql_alchemy import SQLAlchemyRepository
from sqlalchemy import select
from sqlalchemy.orm import contains_eager, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
import logging
from config import env_config



logging.basicConfig(level=env_config.LOG_LEVEL)
logger = logging.getLogger(__name__)


class ReferralsRepository(SQLAlchemyRepository):

    model: Referral = Referral


    @classmethod
    async def find_all(self, session: AsyncSession, referred_by: int):
        try:
            result = await session.execute(
                select(self.model)
                .options(joinedload(self.model.user_ref))
                .where(self.model.referred_by == referred_by)
            )
            referrals = result.scalars().all()
            return referrals
        except (SQLAlchemyError, Exception) as e:
            logger.error(
                f"Ошибка при поиске всех значений в базе данных", extra={"ошибка": e}
            )
            raise e