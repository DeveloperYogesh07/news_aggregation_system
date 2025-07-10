from app.models.article_vote import ArticleVote, VoteType
from sqlalchemy.orm import Session

class VoteRepository:

    @staticmethod
    def add_or_update_vote(db: Session, user_id: int, article_id: int, vote: VoteType):
        existing_vote = db.query(ArticleVote).filter_by(user_id=user_id, article_id=article_id).first()

        if existing_vote:
            existing_vote.vote = vote
        else:
            db.add(ArticleVote(user_id=user_id, article_id=article_id, vote=vote))

        db.commit()

    @staticmethod
    def count_votes(db: Session, article_id: int):
        likes = db.query(ArticleVote).filter_by(article_id=article_id, vote=VoteType.like).count()
        dislikes = db.query(ArticleVote).filter_by(article_id=article_id, vote=VoteType.dislike).count()
        return {"likes": likes, "dislikes": dislikes}
