from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.services.notification_service import NotificationService
from app.schemas.notification import NotificationConfigRead, NotificationConfigUpdate
from app.models.user import User
from app.schemas.notification import NotificationRead
from app.repositories.notification_repository import NotificationRepository


router = APIRouter()


class KeywordsUpdateRequest(BaseModel):
    keywords: list[str]


class EnableOnlyUpdate(BaseModel):
    enabled: bool


@router.get("/", response_model=list[NotificationConfigRead])
def get_notifications(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    service = NotificationService(db)
    return service.get_user_configs(current_user.id)  # type: ignore


@router.put("/keywords")
def update_keywords(
    payload: KeywordsUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotificationService(db)
    service.update_keywords(current_user.id, payload.keywords)  # type: ignore
    return {"message": "Keywords updated"}


@router.put("/{config_id}", response_model=NotificationConfigRead)
def update_config(
    config_id: int,
    data: EnableOnlyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NotificationService(db)
    return service.update_config(config_id, data.enabled)


@router.get("/history", response_model=list[NotificationRead])
def view_notifications(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return NotificationRepository.get_for_user(db, user.id)  # type: ignore
