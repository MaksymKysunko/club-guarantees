from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Role(SQLModel, table=True):
    __tablename__ = "role"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, description="system code, e.g. 'banker','member'")
    name: str = Field(description="display name")
    description: Optional[str] = None
    is_system: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
