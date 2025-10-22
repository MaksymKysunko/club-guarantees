from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoleRead(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    is_system: bool
    created_at: datetime
 
