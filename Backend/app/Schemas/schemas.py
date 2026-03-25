from pydantic import BaseModel, ConfigDict, EmailStr


class CreatorBase(BaseModel):
    email: EmailStr
    userName: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    userName: str
