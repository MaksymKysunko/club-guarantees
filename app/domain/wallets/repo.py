from sqlmodel import Session, select
from .models import Wallet
from typing import Optional

def get_by_user_currency(session: Session, user_id: int, currency: str) -> Wallet | None:
    return session.exec(
        select(Wallet).where(Wallet.user_id == user_id, Wallet.currency == currency)
    ).first()

def get_wallet_by_user_currency(session: Session, user_id: int, currency: str) -> Optional[Wallet]:
    stmt = select(Wallet).where(Wallet.user_id == user_id, Wallet.currency == currency)
    return session.exec(stmt).first()

def create(session: Session, wallet: Wallet) -> Wallet:
    session.add(wallet)
    session.commit()
    session.refresh(wallet)
    return wallet

def list_by_user(session: Session, user_id: int) -> list[Wallet]:
    return session.exec(
        select(Wallet).where(Wallet.user_id == user_id).order_by(Wallet.currency)
    ).all()

def list_all(session: Session) -> list[Wallet]:
    return session.exec(select(Wallet).order_by(Wallet.user_id, Wallet.currency)).all()

