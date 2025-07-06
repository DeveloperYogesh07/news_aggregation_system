from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_user
from app.schemas.vote import VoteCreate
from app.repositories.vote_repository import VoteRepository
from app.models.user import User

router = APIRouter()


@router.post("/")
def vote_article(
    vote_data: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    VoteRepository.add_or_update_vote(db, current_user.id, vote_data.article_id, vote_data.vote)  # type: ignore
    return {"message": f"Your {vote_data.vote} was recorded."}


@router.get("/{article_id}/count")
def get_vote_counts(article_id: int, db: Session = Depends(get_db)):
    return VoteRepository.count_votes(db, article_id)
