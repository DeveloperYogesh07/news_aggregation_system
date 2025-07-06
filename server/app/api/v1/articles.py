from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.services.news_service import NewsService
from app.models.user import User
from app.repositories.article_repository import ArticleRepository
from app.schemas.article import ArticleRead
from app.repositories.vote_repository import VoteRepository
from app.repositories.article_report_repository import ArticleReportRepository
from app.exceptions.custom_exceptions import ArticleException, ExternalAPIException

router = APIRouter()


@router.get("/", response_model=List[ArticleRead])
def list_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        service = NewsService(db)
        return service.get_articles(skip=skip, limit=limit)
    except ArticleException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search", response_model=List[ArticleRead])
def search_articles(query: str = Query(...), db: Session = Depends(get_db)):
    try:
        return ArticleRepository.search(db, query)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/range")
def get_articles_by_date_range(
    start_date: date = Query(...),
    end_date: date = Query(...),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    try:
        return ArticleRepository.get_by_date_range(db, start_date, end_date, category)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to get articles by date range"
        )


@router.get("/date")
def get_articles_by_date(
    date: date = Query(...),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    try:
        return ArticleRepository.get_by_date(db, date, category)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get articles by date")


@router.get("/{article_id}", response_model=ArticleRead)
def get_article(article_id: int, db: Session = Depends(get_db)):
    try:
        service = NewsService(db)
        return service.get_article(article_id)
    except ArticleException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/fetch-external")
def fetch_external_news(
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        service = NewsService(db)
        service.fetch_and_store_top_headlines(category=category)
        return {"message": "News fetched and stored"}
    except ExternalAPIException as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ArticleException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch external news")


@router.get("/votes/{article_id}/count")
def get_vote_count(article_id: int, db: Session = Depends(get_db)):
    try:
        return VoteRepository.count_votes(db, article_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to get vote count")


@router.post("/report/{article_id}")
def report_article(
    article_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        ArticleReportRepository.create(db, article_id, user.id)
        count = ArticleReportRepository.count_reports(db, article_id)

        THRESHOLD = 5
        if count >= THRESHOLD:
            ArticleRepository.hide_article(db, article_id)

        return {"message": "Article reported successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to report article")
