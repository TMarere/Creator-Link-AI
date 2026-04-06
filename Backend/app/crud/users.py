from sqlalchemy.orm import Session

from app.Schemas.schemas import CreatorBase, UserResponse
from app.db.models.users import User


def create_user(db: Session, user: CreatorBase) -> UserResponse:
    db_user = User(email=user.email, userName=user.userName, niche=user.niche)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session) -> list[UserResponse]:
    return db.query(User).order_by(User.userName).all()


def get_connections(
    db: Session, niche: str, exclude_id: int | None = None
) -> list[UserResponse]:
    query = db.query(User).filter(User.niche == niche)
    if exclude_id:
        query = query.filter(User.id != exclude_id)
    return query.order_by(User.userName).all()
