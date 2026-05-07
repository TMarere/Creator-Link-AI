from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.Schemas.schemas import RecommendationPayload
from app.db.models.recommendations import Recommendation
from app.services.llm import generate_content_ideas

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{user_id}")
def get_recommendations(
    user_id: int,
    niche: str | None = None,
    db: Session = Depends(get_db),
):
    rec = (
        db.query(Recommendation)
        .filter(Recommendation.creator_id == user_id)
        .first()
    )
    if rec:
        return RecommendationPayload(
            user_id=user_id,
            short_form=rec.short_form or [],
            long_form=rec.long_form or [],
            deep_dive=rec.deep_dive or [],
            related_creators=rec.similar_creators or [],
        )

    fallback = generate_content_ideas(niche)
    return RecommendationPayload(
        user_id=user_id,
        short_form=fallback.short_form,
        long_form=fallback.long_form,
        deep_dive=fallback.deep_dive,
        related_creators=fallback.related_creators,
    )
