from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime



class User(BaseModel):

    email: EmailStr



class UserRegister(User):
    password: str
    referral_code: str | None = None


class UserLogin(User):
    password: str



class UserOut(User):
    id: int
    registered_at: datetime
    referred_by: int | None = None

    model_config = ConfigDict(from_attributes=True)

    