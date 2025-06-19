from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    content: str

class ArticleCreate(ArticleBase):
    pass

class ArticleRead(ArticleBase):
    id: int

    class Config:
        orm_mode = True
