from sqlmodel import Session
from .schemas import UserCreate
from .models import User
from .repo import get_by_email, add, count_all, set_active, set_role_by_code, find_user_with_role
from app.domain.roles.repo import get_by_code
from app.core.errors import bad_request

def register_user(session: Session, payload: UserCreate) -> User:
    if get_by_email(session, payload.email):
        bad_request("User with this email already exists")
    # перший користувач -> admin + active
    is_first = count_all(session) == 0
    role_code = "admin" if is_first else "member"
    role = get_by_code(session, role_code)
    user = User(email=payload.email, nick=payload.nick, role_id=role.id, is_active=is_first)
    return add(session, user)

def activate_user(session: Session, user_id: int) -> User:
    user = set_active(session, user_id, True)
    if not user: bad_request("User not found")
    return user

def change_user_role(session: Session, user_id: int, role_code: str) -> User:
    if role_code == "banker":
        existing = find_user_with_role(session, "banker")
        if existing and existing.id != user_id:
            bad_request("В системі може бути тільки один БАНКИР")
    user = set_role_by_code(session, user_id, role_code)
    if not user: bad_request("User or role not found")
    return user
