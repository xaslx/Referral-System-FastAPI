from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.referrals import Referral
    from src.models.referral_code import ReferralCode



class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]
    registered_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    referred_by: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=True, default=None)

    referral_codes: Mapped['ReferralCode'] = relationship('ReferralCode', back_populates='user', lazy='joined')
    referrals: Mapped[list['Referral']] = relationship('Referral', foreign_keys='Referral.user_id', back_populates='user_ref')
    referrals_made: Mapped[list['Referral']] = relationship('Referral', foreign_keys='Referral.referred_by', back_populates='referrer')