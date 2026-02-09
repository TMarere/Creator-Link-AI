from pydantic import BaseModel
from typing import List

class CreatorBase(BaseModel):
	username: str
	email: str
	niche: str
	interests: List[str] = []
	
class UserResponse(UserCreator):
	id: int
	
class Config:
    from_attributes = True
