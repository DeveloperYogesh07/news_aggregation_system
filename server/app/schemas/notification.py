from pydantic import BaseModel
from typing import Optional

class NotificationConfigRead(BaseModel):
    id: int
    category: Optional[str]
    keyword: Optional[str]
    enabled: bool

    class Config:
        orm_mode = True

class NotificationConfigUpdate(BaseModel):
    category: Optional[str]
    keyword: Optional[str]
    enabled: bool
