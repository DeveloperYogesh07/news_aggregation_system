from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationRead
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[NotificationRead])
def list_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = NotificationService(db)
    return service.get_notifications_for_user(user_id=current_user.id)
