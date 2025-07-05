from unicodedata import category
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.article import Article
from datetime import date, timedelta
from sqlalchemy import and_
from datetime import datetime, date

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
    

    @staticmethod
    def get_by_date(db: Session, article_date: date, category: str = None):
        query = db.query(Article).filter(Article.created_at >= article_date, Article.created_at < article_date + timedelta(days=1))
        if category:
            query = query.filter(Article.category == category)
        return query.order_by(Article.created_at.desc()).all()

    @staticmethod
    def get_by_date_range(db: Session, start_date: date, end_date: date, category: str = None):
        query = db.query(Article).filter(
            Article.created_at >= datetime.combine(start_date, datetime.min.time()),
            Article.created_at <= datetime.combine(end_date, datetime.max.time())
        )

        if category:
            query = query.filter(Article.category == category)

        return query.order_by(Article.created_at.desc()).all()
