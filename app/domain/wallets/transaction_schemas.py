from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WalletTransactionCreate(BaseModel):
    wallet_id: int
    currency: str
    amount_posted: float = 0.0
    amount_reserved: float = 0.0
    corresponding_wallet_id: int
    deal_id: Optional[int] = None

class WalletTransactionRead(BaseModel):
    id: int
    wallet_id: int
    currency: str
    amount_posted: float
    amount_reserved: float
    corresponding_wallet_id: int
    deal_id: Optional[int]
    created_at: datetime
    changed_at: datetime
