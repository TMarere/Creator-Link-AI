from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.Schemas.schemas import CreatorBase, UserResponse
from app.crud.users import create_user, get_users
from app.api.deps import get_db


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user: CreatorBase, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=list[UserResponse])
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)
