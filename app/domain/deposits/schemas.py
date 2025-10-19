from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DepositCreate(BaseModel):
    currency: str
    amount: float
    note: Optional[str] = None

class DepositRead(BaseModel):
    id: int
    user_id: int
    currency: str
    amount: float
    note: Optional[str]
    status: str
    created_at: datetime
    approved_at: Optional[datetime]
    rejected_at: Optional[datetime]
    decided_by_user_id: Optional[int]
