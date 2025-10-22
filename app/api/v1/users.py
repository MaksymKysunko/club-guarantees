from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import require_admin
from app.domain.users.models import User
from app.domain.users.schemas import UserRead, RoleChange
from app.domain.users.service import activate_user, change_user_role
from app.domain.users.repo import list_all_with_roles

router = APIRouter()

@router.get("/", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session), _admin=Depends(require_admin)):
    return list_all_with_roles(session)

@router.post("/{user_id}/activate", response_model=UserRead)
def activate(user_id: int, session: Session = Depends(get_session), _=Depends(require_admin)):
    return activate_user(session, user_id)

@router.post("/{user_id}/role", response_model=UserRead)
def set_role(user_id: int, payload: RoleChange, session: Session = Depends(get_session), _=Depends(require_admin)):
    return change_user_role(session, user_id, payload.role_code)
