from sqlmodel import Session, select
from .models import Role

def get_by_code(session: Session, code: str) -> Role | None:
    return session.exec(select(Role).where(Role.code == code)).first()

def add(session: Session, role: Role) -> Role:
    session.add(role); session.commit(); session.refresh(role); return role

def ensure_seed(session: Session):
    for code, name in [("admin","Admin"), ("banker","Banker"), ("member","Member")]:
        if not get_by_code(session, code):
            add(session, Role(code=code, name=name, description=f"Default role: {name}", is_system=True))
