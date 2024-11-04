from fastapi import FastAPI
from src.routers.auth import auth_router
from src.routers.referral_code import referral_code_router
from src.routers.referrals import referrals_router


app: FastAPI = FastAPI()

app.include_router(auth_router)
app.include_router(referral_code_router)
app.include_router(referrals_router)






