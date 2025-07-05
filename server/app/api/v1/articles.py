from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.services.news_service import NewsService
from app.models.user import User
from app.repositories.article_repository import ArticleRepository
from app.schemas.article import ArticleRead

router = APIRouter()


@router.get("/", response_model=list[ArticleRead])
def list_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    service = NewsService(db)
    return service.get_articles(skip=skip, limit=limit)

@router.get("/search", response_model=List[ArticleRead])
def search_articles(
    query: str = Query(...),
    db: Session = Depends(get_db)
):
    return ArticleRepository.search(db, query)


@router.get("/{article_id}", response_model=ArticleRead)
def get_article(article_id: int, db: Session = Depends(get_db)):
    service = NewsService(db)
    article = service.get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.post("/fetch-external")
def fetch_external_news(
    category: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = NewsService(db)
    service.fetch_and_store_top_headlines(category=category)
    return {"message": "News fetched and stored"}



