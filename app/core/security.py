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

def require_active(user=Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(403, "User is not active")
    return user

def require_role(role_code: str):
    def _dep(user=Depends(require_active), session: Session = Depends(get_session)):
        role = get_by_code(session, role_code)
        if not role or user.role_id != role.id:
            raise HTTPException(403, f"{role_code} role required")
        return user
    return _dep

require_admin = require_role("admin")
require_banker = require_role("banker")
