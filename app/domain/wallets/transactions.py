from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import CheckConstraint

class WalletTransaction(SQLModel, table=True):
    """
    Журнал змін гаманця:
      - amount_posted  -> впливає на баланс/сальдо
      - amount_reserved-> впливає на резерв (блокування)
    Обов'язковий кореспондентський гаманець (club/member/інший wallet).
    """
    __tablename__ = "wallet_transaction"
    __table_args__ = (
        CheckConstraint("(amount_posted <> 0) OR (amount_reserved <> 0)", name="ck_wtx_nonzero"),
        CheckConstraint("length(currency) > 0", name="ck_wtx_currency_nonempty"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # чий гаманець змінюється
    wallet_id: int = Field(foreign_key="wallet.id", index=True)

    # валюта рядка
    currency: str

    # рухи (знакові; >0 приплив/блок, <0 відтік/розблок)
    amount_posted: float = 0.0
    amount_reserved: float = 0.0

    # кореспондентський гаманець (NOT NULL)
    corresponding_wallet_id: int = Field(foreign_key="wallet.id", index=True)

    # прив'язка до угоди (обов'язкова для резерв/реліз/конфіскації; умовне правило — на рівні бізнес-логіки)
    deal_id: Optional[int] = Field(default=None, foreign_key="deal.id", index=True)

    # часи
    created_at: datetime = Field(default_factory=datetime.utcnow)
    changed_at: datetime = Field(default_factory=datetime.utcnow)
