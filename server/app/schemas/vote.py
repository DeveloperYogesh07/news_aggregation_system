from pydantic import BaseModel
from enum import Enum

class VoteType(str, Enum):
    like = "like"
    dislike = "dislike"

class VoteCreate(BaseModel):
    article_id: int
    vote: VoteType
