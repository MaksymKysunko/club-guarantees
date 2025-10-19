from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class WalletTransaction(SQLModel, table=True):
    __tablename__ = "wallet_transaction"

    id: Optional[int] = Field(default=None, primary_key=True)

    # базова прив'язка
    wallet_id: int = Field(foreign_key="wallet.id", index=True)
    currency: str  # очікувана відповідність wallet.currency

    # тип операції (єдина шкала для всього, що впливає на гаманець)
    tx_type: str  # приклади: deposit_approved, reserve_create, reserve_release, reserve_confiscate, adjust_credit, adjust_debit

    # сума операції (як її декларував ініціатор)
    amount: float

    # фактичний вплив на агрегати гаманця (дельти-кеш)
    balance_delta: float = 0.0   # +/- змінює balance
    reserved_delta: float = 0.0  # +/- змінює reserved

    # опційні зв'язки (для угод/компенсацій)
    deal_id: Optional[int] = Field(default=None, foreign_key="deal.id")
    participant_id: Optional[int] = Field(default=None, foreign_key="deal_participant.id")
    counterparty_wallet_id: Optional[int] = Field(default=None, foreign_key="wallet.id")

    # службове
    note: Optional[str] = None
    status: str = Field(default="posted")  # наприклад: posted|pending (деталізуємо пізніше)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    posted_at: Optional[datetime] = None
    actor_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
