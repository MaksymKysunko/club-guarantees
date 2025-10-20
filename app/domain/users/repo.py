from sqlmodel import Session, select
from .models import User
from app.domain.roles.repo import get_by_code

from sqlalchemy import func
from sqlmodel import Session, select
from .models import User

def count_all(session: Session) -> int:
    # коректний COUNT(*) у стилі SQLAlchemy 2.0
    return session.exec(select(func.count()).select_from(User)).one()

def get_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

def add(session: Session, user: User) -> User:
    session.add(user); session.commit(); session.refresh(user); return user

def get(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def list_all(session: Session) -> list[User]:
    return session.exec(select(User).order_by(User.id)).all()

def set_active(session: Session, user_id: int, active: bool) -> User | None:
    user = session.get(User, user_id)
    if not user: return None
    user.is_active = active
    session.add(user); session.commit(); session.refresh(user)
    return user

def set_role_by_code(session: Session, user_id: int, role_code: str) -> User | None:
    role = get_by_code(session, role_code)
    if not role: return None
    user = session.get(User, user_id)
    if not user: return None
    user.role_id = role.id
    session.add(user); session.commit(); session.refresh(user)
    return user

def find_user_with_role(session: Session, role_code: str) -> User | None:
    role = get_by_code(session, role_code)
    if not role: return None
    return session.exec(select(User).where(User.role_id == role.id)).first()
