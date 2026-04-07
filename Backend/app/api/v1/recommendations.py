from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.Schemas.schemas import RecommendationPayload
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
    payload = generate_recommendations(db, user_id, niche)
    return RecommendationPayload(**payload)
