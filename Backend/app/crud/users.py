from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.Schemas.schemas import CreatorBase, UserResponse
from app.crud.users import create_user, get_users


def createUsers(db: Session, user: CreatorBase) -> UserResponse:
    db_user = CreatorBase(email=user.email, userName=user.userName)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    

   
    def get_users(db: Session):
        return db.query(User).all()

  