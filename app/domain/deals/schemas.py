from pydantic import BaseModel
from typing import List
from datetime import datetime
from sqlmodel import SQLModel, Field

class DealCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    currency: str = Field(min_length=1, max_length=16)
    guarantee_total: float = Field(gt=0)

class DealListItem(SQLModel):
    id: int
    title: str
    currency: str
    guarantee_total: float
    status: str
    created_at: datetime
    participants_count: int

class DealRead(SQLModel):
    id: int
    title: str
    currency: str
    guarantee_total: float
    status: str
    created_at: datetime

class ParticipantAdd(SQLModel):
    user_id: int

class ParticipantRead(SQLModel):
    id: int
    deal_id: int
    user_id: int
    terms_accepted: bool
    done_confirmed: bool

class DealActionCreate(SQLModel):
    description: str = Field(min_length=1, max_length=500)

class DealActionRead(SQLModel):
    id: int
    deal_id: int
    description: str
    creator_id: int
    created_at: datetime
