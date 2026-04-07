from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.Schemas.schemas import CreatorBase, CreatorCard, UserResponse
from app.crud.users import create_user, get_users
from app.db.models.users import User
from app.api.deps import get_db


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user: CreatorBase, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=list[CreatorCard])
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)


@router.get("/me", response_model=UserResponse)
def get_user_by_email(
    email: EmailStr = Query(...), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
