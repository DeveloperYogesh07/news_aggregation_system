from pydantic import BaseModel
from typing import Optional


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass


class ArticleRead(ArticleBase):
    id: int
    title: str
    content: Optional[str]
    url: Optional[str] = None
    category: Optional[str]

    class Config:
        from_attributes = True
