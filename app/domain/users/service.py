from sqlmodel import Session
from .schemas import UserCreate, UserRead
from .models import User
from .repo import get_by_email, add
from app.core.errors import bad_request
from app.domain.roles.repo import get_by_code
from app.domain.roles.schemas import RoleRead

def create_user(session: Session, payload: UserCreate) -> UserRead:
    if get_by_email(session, payload.email):
        bad_request("User with this email already exists")
    role = get_by_code(session, payload.role_code)
    if not role:
        bad_request(f"Unknown role_code: {payload.role_code}")
    user = add(session, User(email=payload.email, nick=payload.nick, role_id=role.id))
    # збагачуємо відповідь рольовим довідником
    return UserRead(
        id=user.id, email=user.email, nick=user.nick, role_id=user.role_id,
        created_at=user.created_at, role=RoleRead(**role.model_dump())
    )
