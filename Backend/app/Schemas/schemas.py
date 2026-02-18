from pydantic import BaseModel, EmailStr

class CreatorBase(BaseModel):
    email: EmailStr
    userName: str

class UserResponse(CreatorBase):
    id: int

    class Config:
        orm_mode = True
