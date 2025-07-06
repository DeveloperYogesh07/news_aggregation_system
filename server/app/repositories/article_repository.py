from sqlalchemy import or_, and_, not_
from sqlalchemy.orm import Session
from app.models.article import Article
from datetime import date, timedelta
from sqlalchemy import and_
from datetime import datetime, date
from app.models.category import Category
from app.models.blacklisted_keyword import BlacklistedKeyword
from typing import Optional


class ArticleRepository:

    @staticmethod
    def get_blacklisted_keywords(db: Session):
        return [kw.keyword.lower() for kw in db.query(BlacklistedKeyword).all()]

    @staticmethod
    def create(
        db: Session,
        title: str,
        content: str,
        url: Optional[str] = None,
        category: str = "general",
    ):
        db_article = Article(
            title=title, content=content, url=url, category=category or "general"
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10):
        blacklist = ArticleRepository.get_blacklisted_keywords(db)

        query = (
            db.query(Article)
            .join(Category, Article.category == Category.name)
            .filter(Article.is_hidden == False, Category.is_hidden == False)
        )

        for kw in blacklist:
            query = query.filter(
                not_(Article.title.ilike(f"%{kw}%")),
                not_(Article.content.ilike(f"%{kw}%")),
            )

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, article_id: int):
        return db.query(Article).filter(Article.id == article_id).first()

    @staticmethod
    def search(db: Session, query_str: str):
        blacklist = ArticleRepository.get_blacklisted_keywords(db)

        query = (
            db.query(Article)
            .join(Category, Article.category == Category.name)
            .filter(
                Article.is_hidden == False,
                Category.is_hidden == False,
                or_(
                    Article.title.ilike(f"%{query_str}%"),
                    Article.content.ilike(f"%{query_str}%"),
                ),
            )
        )

        for kw in blacklist:
            query = query.filter(
                not_(Article.title.ilike(f"%{kw}%")),
                not_(Article.content.ilike(f"%{kw}%")),
            )

        return query.order_by(Article.created_at.desc()).all()

    @staticmethod
    def get_by_date(db: Session, article_date: date, category: Optional[str] = None):
        blacklist = ArticleRepository.get_blacklisted_keywords(db)

        query = (
            db.query(Article)
            .join(Category, Article.category == Category.name)
            .filter(
                Article.created_at >= article_date,
                Article.created_at < article_date + timedelta(days=1),
                Article.is_hidden == False,
                Category.is_hidden == False,
            )
        )

        if category:
            query = query.filter(Article.category == category)

        for kw in blacklist:
            query = query.filter(
                not_(Article.title.ilike(f"%{kw}%")),
                not_(Article.content.ilike(f"%{kw}%")),
            )

        return query.order_by(Article.created_at.desc()).all()

    @staticmethod
    def get_by_date_range(
        db: Session, start_date: date, end_date: date, category: Optional[str] = None
    ):
        blacklist = ArticleRepository.get_blacklisted_keywords(db)

        query = (
            db.query(Article)
            .join(Category, Article.category == Category.name)
            .filter(
                Article.created_at >= datetime.combine(start_date, datetime.min.time()),
                Article.created_at <= datetime.combine(end_date, datetime.max.time()),
                Article.is_hidden == False,
                Category.is_hidden == False,
            )
        )

        if category:
            query = query.filter(Article.category == category)

        for kw in blacklist:
            query = query.filter(
                not_(Article.title.ilike(f"%{kw}%")),
                not_(Article.content.ilike(f"%{kw}%")),
            )

        return query.order_by(Article.created_at.desc()).all()

    @staticmethod
    def hide_article(db, article_id):
        article = db.query(Article).get(article_id)
        if article:
            article.is_hidden = True
            db.commit()

    @staticmethod
    def get_visible_articles(db):
        return db.query(Article).filter_by(is_hidden=False).all()

    @staticmethod
    def filter_articles_by_blacklist(db, blacklist):
        query = db.query(Article).filter(Article.is_hidden == False)
        for word in blacklist:
            query = query.filter(
                ~Article.title.contains(word), ~Article.content.contains(word)
            )
        return query.all()
