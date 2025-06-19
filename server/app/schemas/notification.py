from pydantic import BaseModel

class NotificationRead(BaseModel):
    id: int
    message: str
    is_read: bool

    class Config:
        orm_mode = True
