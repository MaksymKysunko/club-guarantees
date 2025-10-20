from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.core.db import get_session
from app.core.security import require_banker
from app.domain.wallets.schemas import WalletCreate, WalletRead
from app.domain.wallets.service import open_club_wallet, list_wallets_by_user, list_all_wallets
from app.domain.deposits.schemas import DepositRead
from app.domain.deposits.repo import list_by_status as deposits_list_by_status
from app.domain.deposits.service import approve_deposit, reject_deposit

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


@router.get("/deposits", response_model=list[DepositRead])
def list_deposits(status: Optional[str] = Query(default=None), session: Session = Depends(get_session), _banker=Depends(require_banker)):
    return deposits_list_by_status(session, status)

@router.post("/deposits/{deposit_id}/approve", response_model=DepositRead)
def approve_deposit_ep(deposit_id: int, session: Session = Depends(get_session), banker=Depends(require_banker)):
    return approve_deposit(session, deposit_id, banker.id)

@router.post("/deposits/{deposit_id}/reject", response_model=DepositRead)
def reject_deposit_ep(deposit_id: int, session: Session = Depends(get_session), banker=Depends(require_banker)):
    return reject_deposit(session, deposit_id, banker.id)
