from app.models.saved_articles import SavedArticle
from sqlalchemy.orm import Session

class SavedArticleRepository:
    @staticmethod
    def create(db: Session, user_id: int, article_id: int, title: str, content: str, url: str):
        article = SavedArticle(
            user_id=user_id,
            article_id=article_id,
            title=title,
            content=content,
            url=url
        )
        db.add(article)
        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def get_for_user(db: Session, user_id: int):
        return db.query(SavedArticle).filter_by(user_id=user_id).order_by(SavedArticle.created_at.desc()).all()

    @staticmethod
    def delete(db: Session, article_id: int, user_id: int):
        obj = db.query(SavedArticle).filter_by(article_id=article_id, user_id=user_id).first()
        if not obj:
            return False
        db.delete(obj)
        db.commit()
        return True
