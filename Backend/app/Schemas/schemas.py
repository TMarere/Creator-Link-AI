from pydantic import BaseModel, ConfigDict, EmailStr


class CreatorBase(BaseModel):
    email: EmailStr
    userName: str
    niche: str
    instagram: str | None = None
    youtube: str | None = None
    tiktok: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    userName: str
    niche: str
    instagram: str | None = None
    youtube: str | None = None
    tiktok: str | None = None


class CreatorCard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    userName: str
    niche: str
    instagram: str | None = None
    youtube: str | None = None
    tiktok: str | None = None


class RecommendationPayload(BaseModel):
    user_id: int
    short_form: list[str]
    long_form: list[str]
    deep_dive: list[str]
    related_creators: list[str]
