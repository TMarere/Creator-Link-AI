import logging
import math
from typing import Iterable, List

from openai import OpenAI

# openai-python has changed exception import paths across versions.
# Keep this tolerant so local installs don't break at import-time.
try:  # pragma: no cover
    from openai import OpenAIError  # type: ignore
except Exception:  # pragma: no cover
    try:
        from openai.error import OpenAIError  # type: ignore
    except Exception:  # pragma: no cover
        OpenAIError = Exception  # type: ignore

from core.config import settings

logger = logging.getLogger("app.services.embeddings")


def _simple_vector(text: str, size: int = 16) -> List[float]:
    seed = sum(ord(char) for char in text) or 1
    return [((seed * (i + 1)) % 100) / 100.0 for i in range(size)]


def create_embedding(text: str) -> List[float]:
    if not settings.OPENAI_API_KEY:
        logger.warning("Missing OPENAI_API_KEY, using simple fallback embedding.")
        return _simple_vector(text)

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        resp = client.embeddings.create(model="text-embedding-ada-002", input=text)
        return resp.data[0].embedding
    except OpenAIError as exc:
        logger.exception("OpenAI embedding failed, falling back to simple vector", exc_info=exc)
        return _simple_vector(text)


def cosine_similarity(a: Iterable[float], b: Iterable[float]) -> float:
    a_vec = list(a)
    b_vec = list(b)
    dot = sum(x * y for x, y in zip(a_vec, b_vec))
    norm_a = math.sqrt(sum(x * x for x in a_vec))
    norm_b = math.sqrt(sum(y * y for y in b_vec))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
