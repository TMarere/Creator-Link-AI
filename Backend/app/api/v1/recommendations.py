from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.services.recommendation import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{user_id}")
def get_recommendations(
    user_id: int,
    niche: str | None = None,
    db: Session = Depends(get_db),
):
    """
    Return recommendation candidates for a creator.
    """
    return {
        "user_id": user_id,
        "recommendations": generate_recommendations(db, user_id, niche),
    }
