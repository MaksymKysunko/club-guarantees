from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WalletTransactionCreate(BaseModel):
    wallet_id: int
    currency: str
    tx_type: str
    amount: float
    deal_id: Optional[int] = None
    participant_id: Optional[int] = None
    counterparty_wallet_id: Optional[int] = None
    note: Optional[str] = None

class WalletTransactionRead(BaseModel):
    id: int
    wallet_id: int
    currency: str
    tx_type: str
    amount: float
    balance_delta: float
    reserved_delta: float
    deal_id: Optional[int]
    participant_id: Optional[int]
    counterparty_wallet_id: Optional[int]
    note: Optional[str]
    status: str
    created_at: datetime
    posted_at: Optional[datetime]
    actor_user_id: Optional[int]
