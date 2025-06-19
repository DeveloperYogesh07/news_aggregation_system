from sqlalchemy.orm import Session
from app.models.saved_articles import SavedArticle

class SavedArticleRepository:

    @staticmethod
    def create(db: Session, user_id: int, title: str, content: str = None, url: str = None):
        saved_article = SavedArticle(user_id=user_id, title=title, content=content, url=url)
        db.add(saved_article)
        db.commit()
        db.refresh(saved_article)
        return saved_article

    @staticmethod
    def get_for_user(db: Session, user_id: int):
        return db.query(SavedArticle).filter(SavedArticle.user_id == user_id).all()

    @staticmethod
    def delete(db: Session, article_id: int, user_id: int):
        article = db.query(SavedArticle).filter(SavedArticle.id == article_id, SavedArticle.user_id == user_id).first()
        if article:
            db.delete(article)
            db.commit()
            return True
        return False
