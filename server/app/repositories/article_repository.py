from unicodedata import category
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.article import Article

class ArticleRepository:

    @staticmethod
    def create(db: Session, title: str, content: str, url: str = None, category: str = "general"):
        db_article = Article(title=title, content=content,url= url,category=category or "general")
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Article).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, article_id: int):
        return db.query(Article).filter(Article.id == article_id).first()

    @staticmethod
    def search(db: Session, query: str):
        return db.query(Article).filter(
            or_(
                Article.title.ilike(f"%{query}%"),
                Article.content.ilike(f"%{query}%")
            )
        ).order_by(Article.created_at.desc()).all()