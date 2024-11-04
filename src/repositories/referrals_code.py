from src.models.referral_code import ReferralCode
from src.repositories.sql_alchemy import SQLAlchemyRepository




class ReferralCodeRepository(SQLAlchemyRepository):

    model: ReferralCode = ReferralCode