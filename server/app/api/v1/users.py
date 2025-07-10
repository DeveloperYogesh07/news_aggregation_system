from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.schemas.user import UserRead
from app.models.user import User
from app.core.database import get_db

router = APIRouter()


@router.get("/me", response_model=UserRead)
def get_me(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    db.refresh(current_user)
    return current_user
