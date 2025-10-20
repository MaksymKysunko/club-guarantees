from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import require_active
from app.domain.deposits.schemas import DepositCreate, DepositRead
from app.domain.deposits.service import create_deposit_request

router = APIRouter()

@router.post("/", response_model=DepositRead)
def create_deposit(payload: DepositCreate, session: Session = Depends(get_session), user=Depends(require_active)):
    return create_deposit_request(session, user.id, payload.currency, payload.amount, payload.note)
