from sqlalchemy import Column, Integer, String

from app.core.database import Base


class BlacklistedKeyword(Base):
    __tablename__ = "blacklisted_keywords"

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True)
