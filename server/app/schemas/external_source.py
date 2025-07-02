from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ExternalSourceBase(BaseModel):
    name: str
    base_url: str
    api_key: str | None = None
    is_active: bool = True

class ExternalSourceCreate(ExternalSourceBase):
    pass

class ExternalSourceUpdate(BaseModel):
    name: str | None = None
    base_url: str | None = None
    api_key: str | None = None
    is_active: bool | None = None

class ExternalSourceRead(ExternalSourceBase):
    id: int
    last_accessed: Optional[datetime]

    class Config:
        from_attributes = True
