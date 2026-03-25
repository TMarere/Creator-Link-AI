from sqlalchemy.orm import Session

from app.Schemas.schemas import CreatorBase, UserResponse
from app.db.models.users import User


def create_user(db: Session, user: CreatorBase) -> UserResponse:
    db_user = User(email=user.email, userName=user.userName)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session) -> list[UserResponse]:
    return db.query(User).all()
