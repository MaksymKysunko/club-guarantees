from sqlmodel import Session
from .models import Wallet
from .repo import get_by_user_currency, create, list_by_user
from app.domain.users.repo import get as get_user
from .repo import list_all as repo_list_all

def list_all_wallets(session: Session) -> list[Wallet]:
    return repo_list_all(session)

def _account_code(nick: str, currency: str) -> str:
    ccy = currency.upper()
    nick_cropped = (nick or "").strip()[:120]
    return f"ACC.{nick_cropped}.{ccy}"

def open_wallet_for_user(session: Session, user_id: int, currency: str) -> Wallet:
    ccy = currency.upper()
    existing = get_by_user_currency(session, user_id, ccy)
    if existing:
        return existing
    user = get_user(session, user_id)
    account_code = _account_code(user.nick, ccy)
    wallet = Wallet(user_id=user_id, currency=ccy, account_code=account_code)
    return create(session, wallet)

# banker-версія тепер просто делегує
def open_club_wallet(session: Session, banker_user_id: int, currency: str) -> Wallet:
    return open_wallet_for_user(session, banker_user_id, currency)

def list_wallets_by_user(session: Session, user_id: int) -> list[Wallet]:
    return list_by_user(session, user_id)
