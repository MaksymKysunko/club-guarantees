from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Wallet(SQLModel, table=True):
    __tablename__ = "wallet"
    id: Optional[int] = Field(default=None, primary_key=True)

    # власник і система
    user_id: int = Field(foreign_key="user.id", index=True)
    currency: str = Field(index=True)  # 'USDT','BTC','ETH', ...

    # службові атрибути
    account_code: str                  # формат "2600НІК.ВАЛ"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_tx_at: Optional[datetime] = None

    # агрегати (кеш)
    balance: float = 0.0               # підтверджене сальдо
    reserved: float = 0.0              # сукупний активний резерв
