from sqlalchemy.orm import Session

from app.db.models.users import User


def generate_recommendations(db: Session, user_id: int, niche: str | None = None):
    """
    Simple recommendation engine that prioritizes creators inside the same niche
    and falls back to placeholder names when there are no peers yet.
    """
    base = ["Creator A", "Creator B", "Creator C"]
    query = db.query(User).filter(User.id != user_id)
    if niche:
        query = query.filter(User.niche == niche)
    candidates = query.order_by(User.userName).limit(5).all()

    names = [f"{creator.userName} · {creator.niche}" for creator in candidates]
    ordered = []
    seen = set()
    for entry in names + base:
        if entry in seen:
            continue
        seen.add(entry)
        ordered.append(entry)
    return ordered
