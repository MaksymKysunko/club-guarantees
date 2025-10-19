from sqlmodel import Session, select
from .models import User

def get_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

def add(session: Session, user: User) -> User:
    session.add(user); session.commit(); session.refresh(user); return user

def get(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)
