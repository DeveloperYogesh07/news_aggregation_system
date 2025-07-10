from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from app.core.database import Base

class ArticleReport(Base):
    __tablename__ = "article_reports"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
