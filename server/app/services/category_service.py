from app.models.category import Category
from app.schemas.category import CategoryCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class CategoryService:
    def __init__(self, db):
        self.db = db

    def create(self, data: CategoryCreate):
        from app.models.category import Category

        category = Category(name=data.name)
        self.db.add(category)
        try:
            self.db.commit()
            self.db.refresh(category)
            return category
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Category '{data.name}' already exists."
            )
        
    def get_all(self):
        return self.db.query(Category).all()