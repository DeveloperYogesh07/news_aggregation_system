from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_admin_user
from app.models.user import User
from app.services.external_source_service import ExternalSourceService
from app.schemas.external_source import (
    ExternalSourceCreate,
    ExternalSourceRead,
    ExternalSourceUpdate,
)
from app.schemas.category import CategoryCreate, CategoryRead
from app.services.category_service import CategoryService
from app.models.article_report import ArticleReport
from app.models.blacklisted_keyword import BlacklistedKeyword
from app.models.category import Category
from app.repositories.article_repository import ArticleRepository
from pydantic import BaseModel

router = APIRouter()


class BlacklistKeywordRequest(BaseModel):
    keyword: str


@router.post("/external-sources/", response_model=ExternalSourceRead)
def create_external_source(
    data: ExternalSourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    service = ExternalSourceService(db)
    return service.create(data)


@router.get("/external-sources/", response_model=list[ExternalSourceRead])
def list_external_sources(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)
):
    service = ExternalSourceService(db)
    return service.list_sources()


@router.delete("/external-sources/{source_id}")
def delete_external_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    service = ExternalSourceService(db)
    source = service.delete(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return {"message": "Deleted"}


@router.put("/external-sources/{source_id}", response_model=ExternalSourceRead)
def update_external_source(
    source_id: int,
    data: ExternalSourceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    service = ExternalSourceService(db)
    updated = service.update(source_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Source not found")
    return updated


@router.post("/categories/", response_model=CategoryRead)
def add_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    service = CategoryService(db)
    return service.create(data)


@router.get("/categories/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_all()


@router.get("/reported-articles")
def get_reported_articles(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)
):
    return db.query(ArticleReport).all()


@router.put("/articles/{article_id}/hide")
def hide_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    ArticleRepository.hide_article(db, article_id)
    return {"message": "Article hidden"}


@router.put("/categories/{category_id}/hide")
def hide_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    category = db.query(Category).get(category_id)
    if category:
        category.is_hidden = True
        db.commit()
        return {"message": "Category hidden"}


@router.post("/blacklist-keyword")
def add_blacklist_keyword(
    data: BlacklistKeywordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    keyword = data.keyword.strip().lower()
    existing = db.query(BlacklistedKeyword).filter_by(keyword=keyword).first()
    if existing:
        raise HTTPException(
            status_code=400, detail=f"'{keyword}' is already blacklisted."
        )

    db.add(BlacklistedKeyword(keyword=keyword))
    db.commit()
    return {"message": f"'{keyword}' added to blacklist"}
