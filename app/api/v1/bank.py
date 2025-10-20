from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import require_banker
from app.domain.wallets.schemas import WalletCreate, WalletRead
from app.domain.wallets.service import open_club_wallet, list_wallets_by_user, list_all_wallets

router = APIRouter()

@router.post("/wallets", response_model=WalletRead)
def open_bank_wallet(payload: WalletCreate, session: Session = Depends(get_session), banker=Depends(require_banker)):
    return open_club_wallet(session, banker.id, payload.currency)

@router.get("/wallets", response_model=list[WalletRead])
def list_bank_wallets(session: Session = Depends(get_session), banker=Depends(require_banker)):
    return list_wallets_by_user(session, banker.id)

@router.get("/wallets/all", response_model=list[WalletRead])
def list_all_bank_wallets(session: Session = Depends(get_session), _banker=Depends(require_banker)):
    return list_all_wallets(session)