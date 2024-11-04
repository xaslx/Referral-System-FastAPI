from pydantic import BaseModel, ConfigDict
from src.schemas.user import UserOut


class ReferralSchema(BaseModel):
    user_id: int
    referred_by: int
    
class ReferralOutSchema(ReferralSchema):
    id: int
    user_ref: UserOut

    model_config = ConfigDict(from_attributes=True)

