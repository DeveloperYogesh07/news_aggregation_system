from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.category import CategoryRead
from app.services.category_service import CategoryService
from typing import List
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db),current_user: User = Depends(get_current_user) ):
    service = CategoryService(db)
    return service.get_all()
