from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base

class ExternalSource(Base):
    __tablename__ = "external_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    base_url = Column(String, nullable=False)
    api_key = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    last_accessed = Column(DateTime, nullable=True)
