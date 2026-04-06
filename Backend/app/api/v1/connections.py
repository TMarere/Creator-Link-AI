from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud.users import get_connections

router = APIRouter(prefix="/connections", tags=["Connections"])


@router.get("/")
def list_connections(
    niche: str = Query(..., min_length=2),
    exclude_id: int | None = Query(None, alias="excludeId"),
    db: Session = Depends(get_db),
):
    """List nearby creators in the same niche so users can connect."""
    return get_connections(db, niche, exclude_id)
