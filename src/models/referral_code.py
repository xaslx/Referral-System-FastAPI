from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base
from datetime import timedelta
from src.models.user import User



class ReferralCode(Base):
    __tablename__ = 'referral_codes'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    referral_code: Mapped[str | None] = mapped_column(unique=True, nullable=True, default=None)
    expiration_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now() + timedelta(days=15))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship('User', back_populates='referral_codes', lazy='joined')