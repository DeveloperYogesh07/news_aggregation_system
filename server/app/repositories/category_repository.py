from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Category).filter(Category.name == name).first()

    @staticmethod
    def create_if_not_exists(db: Session, name: str):
        existing = CategoryRepository.get_by_name(db, name)
        if not existing:
            category = Category(name=name)
            db.add(category)
            db.commit()
            db.refresh(category)
            return category
        return existing
