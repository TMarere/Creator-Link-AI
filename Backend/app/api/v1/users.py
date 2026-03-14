from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.Schemas.schemas import CreatorBase, UserResponse
from app.crud.users import create_user, get_users
from app.api.deps import get_db


