from sqlachemy import Column, Integer, String, DateTime
from app.database import Base

Class User(Base):
__tablename__ = "users"



__tablename__ = "users"
id = Column(Integer, primary_key=True, index=True)

username = Column(String, unique=True, index=True)

email = Column(String, unique=True, index=True)

instagram_handle = Column(String, unique=True, index=True)