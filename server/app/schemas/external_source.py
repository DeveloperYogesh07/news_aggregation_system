from pydantic import BaseModel

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

    class Config:
        from_attributes = True
