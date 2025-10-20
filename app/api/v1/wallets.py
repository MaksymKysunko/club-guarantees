from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import require_active
from app.domain.wallets.schemas import WalletCreate, WalletRead
from app.domain.wallets.service import open_wallet_for_user, list_wallets_by_user

router = APIRouter()

@router.get("/", response_model=list[WalletRead])
def list_my_wallets(session: Session = Depends(get_session), user=Depends(require_active)):
    return list_wallets_by_user(session, user.id)

@router.post("/", response_model=WalletRead)
def open_my_wallet(payload: WalletCreate, session: Session = Depends(get_session), user=Depends(require_active)):
    return open_wallet_for_user(session, user.id, payload.currency)
