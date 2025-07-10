from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.schemas.saved_articles import SavedArticleCreate, SavedArticleRead
from app.repositories.saved_article_repository import SavedArticleRepository
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=SavedArticleRead)
def create_saved_article(
    article_in: SavedArticleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return SavedArticleRepository.create(
        db=db,
        user_id=current_user.id,  # type: ignore
        article_id=article_in.article_id,
        title=article_in.title,
        content=article_in.content or "",
        url=str(article_in.url) if article_in.url else "",
    )


@router.get("/", response_model=list[SavedArticleRead])
def list_saved_articles(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return SavedArticleRepository.get_for_user(db=db, user_id=current_user.id)  # type: ignore


@router.delete("/{article_id}", status_code=204)
def delete_saved_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    success = SavedArticleRepository.delete(
        db=db, article_id=article_id, user_id=current_user.id  # type: ignore
    )
    if not success:
        raise HTTPException(status_code=404, detail="Saved article not found")
