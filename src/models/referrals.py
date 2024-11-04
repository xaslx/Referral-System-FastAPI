from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base
from src.models.user import User



class Referral(Base):
    __tablename__ = 'referrals'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    referred_by: Mapped[int] = mapped_column(ForeignKey('users.id'))


    user_ref: Mapped['User'] = relationship('User', foreign_keys=[user_id], back_populates='referrals')
    referrer: Mapped['User'] = relationship('User', foreign_keys=[referred_by], back_populates='referrals_made')