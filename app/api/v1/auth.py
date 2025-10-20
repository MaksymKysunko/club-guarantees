from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.domain.users.schemas import UserCreate, UserRead
from app.domain.users.service import register_user

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(payload: UserCreate, session: Session = Depends(get_session)):
    user = register_user(session, payload)
    return user
