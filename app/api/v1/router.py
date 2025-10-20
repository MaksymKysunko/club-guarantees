from fastapi import APIRouter
from . import users, wallets, deposits, deals, arbitration, auth

api_v1 = APIRouter()
api_v1.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1.include_router(users.router, prefix="/users", tags=["users"])
api_v1.include_router(wallets.router, prefix="/wallets", tags=["wallets"])
api_v1.include_router(deposits.router, prefix="/deposits", tags=["deposits"])
api_v1.include_router(deals.router, prefix="/deals", tags=["deals"])
api_v1.include_router(arbitration.router, prefix="/arbitration", tags=["arbitration"])
