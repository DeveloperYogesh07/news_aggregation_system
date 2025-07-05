from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.core.database import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationConfigRead, NotificationConfigUpdate
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=list[NotificationConfigRead])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = NotificationService(db)
    return service.get_user_configs(current_user.id)

@router.put("/{config_id}", response_model=NotificationConfigRead)
def update_config(config_id: int, data: NotificationConfigUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = NotificationService(db)
    return service.update_config(config_id, data.enabled)

@router.put("/keywords")
def update_keywords(keywords: list[str], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    service = NotificationService(db)
    service.update_keywords(current_user.id, keywords)
    return {"message": "Keywords updated"}
