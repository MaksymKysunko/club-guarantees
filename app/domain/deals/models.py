from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Deal(SQLModel, table=True):
    __tablename__ = "deal"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    currency: str                       # MVP: одна валюта на угоду
    guarantee_total: float              # сума гарантії на УЧАСНИКА
    status: str = Field(                # draft|terms_accepted|funding|funded|in_arbitration|completed|cancelled
        default="draft",
        description="draft|terms_accepted|funding|funded|in_arbitration|completed|cancelled"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)

class DealParticipant(SQLModel, table=True):
    __tablename__ = "deal_participant"
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    terms_accepted: bool = False        # акцепт умов угоди
    done_confirmed: bool = False        # підтвердження виконання

class DealAction(SQLModel, table=True):
    __tablename__ = "deal_action"
    id: Optional[int] = Field(default=None, primary_key=True)
    deal_id: int = Field(foreign_key="deal.id", index=True)
    description: str
    creator_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

