from sqlalchemy import Column, Integer, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class VoteType(str, enum.Enum):
    like = "like"
    dislike = "dislike"

class ArticleVote(Base):
    __tablename__ = "article_votes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False)
    vote = Column(Enum(VoteType), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "article_id", name="uix_user_article_vote"),)

    user = relationship("User", back_populates="article_votes")
    article = relationship("Article", back_populates="votes")
