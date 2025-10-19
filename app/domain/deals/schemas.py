from pydantic import BaseModel
from typing import List
from datetime import datetime

class DealCreate(BaseModel):
    title: str
    currency: str
    guarantee_total: float
    actions: List[str] = []             # початковий чекліст (опційно)

class DealRead(BaseModel):
    id: int
    title: str
    currency: str
    guarantee_total: float
    status: str
    created_at: datetime

class DealParticipantRead(BaseModel):
    id: int
    deal_id: int
    user_id: int
    terms_accepted: bool
    done_confirmed: bool

class DealActionRead(BaseModel):
    id: int
    deal_id: int
    description: str
    creator_id: int
    created_at: datetime
