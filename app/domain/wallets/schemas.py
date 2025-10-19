from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WalletCreate(BaseModel):
    currency: str

class WalletRead(BaseModel):
    id: int
    user_id: int
    currency: str
    account_code: str
    created_at: datetime
    last_tx_at: Optional[datetime]
    balance: float
    reserved: float

class WalletWithAvailable(WalletRead):
    available: float
