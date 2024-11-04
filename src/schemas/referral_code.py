from pydantic import BaseModel



class ReferralCodeSchema(BaseModel):
    user_id: int
    referral_code: str | None = None

