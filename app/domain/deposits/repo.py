from typing import Optional
from sqlmodel import Session, select
from .models import DepositRequest

def add(session: Session, dr: DepositRequest) -> DepositRequest:
    session.add(dr); session.commit(); session.refresh(dr); return dr

def get(session: Session, deposit_id: int) -> Optional[DepositRequest]:
    return session.get(DepositRequest, deposit_id)

def list_by_status(session: Session, status: Optional[str] = None) -> list[DepositRequest]:
    stmt = select(DepositRequest).order_by(DepositRequest.created_at.desc())
    if status:
        stmt = stmt.where(DepositRequest.status == status)
    return session.exec(stmt).all()

def set_status_approved(session: Session, dr: DepositRequest, banker_user_id: int):
    from datetime import datetime
    dr.status = "approved"
    dr.decided_by_user_id = banker_user_id
    dr.approved_at = datetime.utcnow()
    session.add(dr)

def set_status_rejected(session: Session, dr: DepositRequest, banker_user_id: int):
    from datetime import datetime
    dr.status = "rejected"
    dr.decided_by_user_id = banker_user_id
    dr.rejected_at = datetime.utcnow()
    session.add(dr)
