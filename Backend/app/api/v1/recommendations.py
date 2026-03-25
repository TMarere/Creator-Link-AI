from fastapi import APIRouter

from app.services.recommendation import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/{user_id}")
def get_recommendations(user_id: int):
    """
    Return recommendation candidates for a creator.
    """
    return {"user_id": user_id, "recommendations": generate_recommendations(user_id)}
