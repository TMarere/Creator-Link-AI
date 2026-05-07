from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"), unique=True)
    niche = Column(String)
    short_form = Column(JSON, nullable=False, default=list)
    long_form = Column(JSON, nullable=False, default=list)
    deep_dive = Column(JSON, nullable=False, default=list)
    similar_creators = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="recommendation")
