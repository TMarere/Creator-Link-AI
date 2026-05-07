from sqlalchemy import Column, Integer, JSON, String
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    userName = Column(String)
    niche = Column(String)
    instagram = Column(String, nullable=True)
    youtube = Column(String, nullable=True)
    tiktok = Column(String, nullable=True)
    embedding = Column(JSON, nullable=True)
    niche = Column(String)
