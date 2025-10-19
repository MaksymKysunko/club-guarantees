from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class DepositRequest(SQLModel, table=True):
    __tablename__ = "deposit_request"

    id: Optional[int] = Field(default=None, primary_key=True)

    # хто і в якій системі вніс
    user_id: int = Field(foreign_key="user.id", index=True)
    currency: str

    # сума та службова інфа
    amount: float
    note: Optional[str] = None

    # статус життєвого циклу заявки
    status: str = Field(
        default="pending",
        description="pending|approved|rejected"
    )

    # таймстемпи
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None

    # хто затвердив/відхилив (банкір), якщо застосовно
    decided_by_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
