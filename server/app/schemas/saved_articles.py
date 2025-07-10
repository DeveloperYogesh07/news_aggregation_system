from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class SavedArticleCreate(BaseModel):
    article_id: int
    title: str
    content: Optional[str] = None
    url: Optional[HttpUrl] = None


class SavedArticleRead(SavedArticleCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
