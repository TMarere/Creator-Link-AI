from sqlalchemy.orm import Session
from app.db.models.users import User

def create_User(db: Session, email: str, name: str):
    db_user = User(email=email, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_User(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()