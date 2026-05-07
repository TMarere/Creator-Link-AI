import json
import logging
from dataclasses import dataclass
from typing import List

from openai import OpenAI
from openai.error import OpenAIError

from app.core.config import settings

logger = logging.getLogger("app.services.llm")

@dataclass
class ContentIdeas:
    short_form: List[str]
    long_form: List[str]
    deep_dive: List[str]
    related_creators: List[str]

IDEA_TEMPLATES = {
    "short_form": {
        "default": [
            "Share a 30-second behind-the-scenes clip of your process.",
            "Drop a quick tip about your niche with a hook."
        ]
    },
    "long_form": {
        "default": [
            "Publish a mini-masterclass detailing your workflow.",
            "Break down a challenge you solved for clients."
        ]
    },
    "deep_dive": {
        "default": [
            "Document a multi-part series exploring emerging trends.",
            "Host an expert roundtable and share the transcript."
        ]
    },
}

PROMPT = """You are a content strategist helping creators grow.
Given a niche, produce three categories of ideas: short_form (snackable clips),
long_form (tutorials, discussions), and deep_dive (research or extended stories).
Respond with JSON: {"short_form":[...],"long_form":[...],"deep_dive":[...],"related_creators":[...]}"""


def _fallback(niche: str) -> ContentIdeas:
    short = IDEA_TEMPLATES["short_form"]["default"]
    long = IDEA_TEMPLATES["long_form"]["default"]
    deep = IDEA_TEMPLATES["deep_dive"]["default"]
    related = [f"{niche.title()} Creator X", f"{niche.title()} Creator Y"] if niche else []
    return ContentIdeas(short_form=list(short), long_form=list(long), deep_dive=list(deep), related_creators=related)


def generate_content_ideas(niche: str | None) -> ContentIdeas:
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY missing; returning fallback content ideas.")
        return _fallback(niche or "")

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    body = f"{PROMPT}\n\nniche: {niche or 'general'}"
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You craft multi-format content ideas."},
                {"role": "user", "content": body},
            ],
            temperature=0.6,
        )
        text = completion.choices[0].message.content
        payload = json.loads(text)
        return ContentIdeas(
            short_form=payload.get("short_form", []),
            long_form=payload.get("long_form", []),
            deep_dive=payload.get("deep_dive", []),
            related_creators=payload.get("related_creators", []),
        )
    except (OpenAIError, json.JSONDecodeError) as exc:
        logger.exception("LLM call failed; returning fallback ideas", exc_info=exc)
        return _fallback(niche or "")
