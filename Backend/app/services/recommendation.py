from sqlalchemy.orm import Session

from app.db.models.users import User

TEMPLATES = {
    "fashion": {
        "short": [
            "30-second styling drop for capsule wardrobes",
            "Street style highlight with user voiceover",
        ],
        "long": [
            "Walk-through of sustainable fabrics and why they matter",
            "Interview mini-doc covering a local designer’s process",
        ],
        "deep": [
            "Long-form analysis of seasonal color psychology",
            "Panel discussion on bridging couture and mass-market",
        ],
    },
    "ai": {
        "short": [
            "Fast breakdown of one prompt that beat GPT’s baseline",
            "Recreate a famous algorithm in a 30-second clip",
        ],
        "long": [
            "Deep dive on how embeddings power your matching logic",
            "Interview a builder shipping an LLM-powered tool",
        ],
        "deep": [
            "Essay-style roadmap for ethical AI content creation",
            "Breakdown of retraining workflows for non-coders",
        ],
    },
    "default": {
        "short": [
            "Quick tip for turning your niche story into a TikTok hook",
            "Share one behind-the-scenes detail from today",
        ],
        "long": [
            "Create a how-to or masterclass with actionable steps",
            "Produce a narrative case study that reflects your growth",
        ],
        "deep": [
            "Write or record a 5-step strategy playbook for peers",
            "Host a live session that answers top community questions",
        ],
    },
}


def build_ideas(niche: str | None, field: str) -> list[str]:
    key = (niche or "default").lower()
    template = TEMPLATES.get(key, TEMPLATES["default"])
    return [idea for idea in template[field]]


def generate_recommendations(
    db: Session, user_id: int, niche: str | None = None
) -> dict[str, list[str]]:
    query = db.query(User).filter(User.id != user_id)
    if niche:
        query = query.filter(User.niche == niche)
    peers = query.order_by(User.userName).limit(5).all()
    related = [f"{creator.userName} · {creator.niche}" for creator in peers]
    short_form = build_ideas(niche, "short")
    long_form = build_ideas(niche, "long")
    deep_dive = build_ideas(niche, "deep")

    return {
        "user_id": user_id,
        "short_form": short_form,
        "long_form": long_form,
        "deep_dive": deep_dive,
        "related_creators": related,
    }
