from fastapi import Depends, Header, HTTPException
from sqlmodel import Session
from app.core.db import get_session
from app.domain.users.repo import get as get_user
from app.domain.roles.repo import get_by_code

def get_current_user(x_user_id: int | None = Header(None), session: Session = Depends(get_session)):
    if not x_user_id:
        raise HTTPException(401, "Provide X-User-Id")
    user = get_user(session, int(x_user_id))
    if not user:
        raise HTTPException(401, "User not found")
    return user

def require_banker(user=Depends(get_current_user), session: Session = Depends(get_session)):
    banker = get_by_code(session, "banker")
    if not banker or user.role_id != banker.id:
        raise HTTPException(403, "Banker role required")
    return user
