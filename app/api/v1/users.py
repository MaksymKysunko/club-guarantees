from fastapi import APIRouter, Depends

from app.core.db import get_session


router = APIRouter()

@router.get("/health")
def users_health():
    return {"ok": True}


