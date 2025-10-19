from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "user"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    nick: str
    role_id: int = Field(foreign_key="role.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
