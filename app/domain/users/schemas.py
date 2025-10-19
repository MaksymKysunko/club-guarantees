from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.domain.roles.schemas import RoleRead

class UserCreate(BaseModel):
    email: EmailStr
    nick: str
    role_code: str = "member"   # приймаємо код ролі, мапимо на role_id

class UserRead(BaseModel):
    id: int
    email: EmailStr
    nick: str
    role_id: int
    created_at: datetime
    role: Optional[RoleRead] = None   # зручно повертати вбудовано
