from datetime import datetime
from sqlmodel import Session
from app.core.errors import bad_request
from .models import DepositRequest
from .repo import add as repo_add, get as repo_get, set_status_approved, set_status_rejected
from app.domain.wallets.service import open_wallet_for_user
from app.domain.wallets.repo import get_by_user_currency
from app.domain.wallets.models import Wallet
from app.domain.wallets.transactions import WalletTransaction

def create_deposit_request(session: Session, user_id: int, currency: str, amount: float, note: str | None) -> DepositRequest:
    if amount is None or amount <= 0:
        bad_request("Amount must be > 0")
    ccy = currency.upper()
    # відкриваємо користувачу гаманець за потреби (ACC.<nick>.<CCY>)
    open_wallet_for_user(session, user_id, ccy)
    dr = DepositRequest(user_id=user_id, currency=ccy, amount=amount, note=note, status="pending")
    return repo_add(session, dr)

def approve_deposit(session: Session, deposit_id: int, banker_user_id: int) -> DepositRequest:
    dr = repo_get(session, deposit_id)
    if not dr:
        bad_request("Deposit request not found")
    if dr.status != "pending":
        bad_request("Deposit request is not pending")

    ccy = dr.currency.upper()

    # гаманець користувача (гарантуємо існування)
    member_wallet = get_by_user_currency(session, dr.user_id, ccy)
    if not member_wallet:
        # відкриваємо, якщо з якихось причин не створився на етапі створення заявки
        member_wallet = open_wallet_for_user(session, dr.user_id, ccy)

    # знайти клубний гаманець банкіра в цій валюті (має бути створений раніше)
    club_wallet = get_by_user_currency(session, banker_user_id, ccy)
    if not club_wallet:
        bad_request("Club wallet for this currency does not exist. Banker must open it first.")

    amount = float(dr.amount)
    now = datetime.utcnow()

    # DOUBLE-ENTRY у журналі транзакцій (одна БД-транзакція)
    t_member = WalletTransaction(
        wallet_id=member_wallet.id,
        currency=ccy,
        amount_posted=amount,
        amount_reserved=0.0,
        corresponding_wallet_id=club_wallet.id,
        deal_id=None,
        created_at=now,
        changed_at=now,
    )
    t_club = WalletTransaction(
        wallet_id=club_wallet.id,
        currency=ccy,
        amount_posted=amount,
        amount_reserved=0.0,
        corresponding_wallet_id=member_wallet.id,
        deal_id=None,
        created_at=now,
        changed_at=now,
    )

    session.add(t_member)
    session.add(t_club)

    # оновити кеш у гаманцях
    member_wallet.balance += amount
    member_wallet.last_tx_at = now
    club_wallet.balance += amount
    club_wallet.last_tx_at = now
    session.add(member_wallet)
    session.add(club_wallet)

    # статус заявки
    set_status_approved(session, dr, banker_user_id)

    # commit всього
    session.commit()
    session.refresh(dr)
    return dr

def reject_deposit(session: Session, deposit_id: int, banker_user_id: int) -> DepositRequest:
    dr = repo_get(session, deposit_id)
    if not dr:
        bad_request("Deposit request not found")
    if dr.status != "pending":
        bad_request("Deposit request is not pending")
    set_status_rejected(session, dr, banker_user_id)
    session.commit()
    session.refresh(dr)
    return dr
