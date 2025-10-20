from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.domain.roles.schemas import RoleRead

class UserCreate(BaseModel):
    email: EmailStr
    nick: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    nick: str
    role_id: int
    is_active: bool
    created_at: datetime

class RoleChange(BaseModel):
    role_code: str  # "admin" | "member" | "banker"

