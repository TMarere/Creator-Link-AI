import json
import logging
from dataclasses import dataclass
from typing import List

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

logger = logging.getLogger("app.services.llm")

@dataclass
class ContentIdeas:
    short_form: List[str]
    long_form: List[str]
    deep_dive: List[str]
    related_creators: List[str]

NICHE_ALIASES = {
    "ai": "ai",
    "artificial intelligence": "ai",
    "machine learning": "ai",
    "fashion": "fashion",
    "style": "fashion",
    "beauty": "beauty",
    "makeup": "beauty",
    "skincare": "beauty",
    "fitness": "fitness",
    "gym": "fitness",
    "health": "wellness",
    "wellness": "wellness",
    "self care": "wellness",
    "travel": "travel",
    "food": "food",
    "cooking": "food",
    "tech": "tech",
    "technology": "tech",
    "gaming": "gaming",
    "finance": "finance",
    "money": "finance",
    "business": "business",
    "entrepreneurship": "business",
}

IDEA_TEMPLATES = {
    "default": {
        "short_form": [
            "Share a fast myth-vs-reality take about {niche}.",
            "Film a 20-second behind-the-scenes moment from your {niche} workflow.",
            "Turn one beginner mistake in {niche} into a punchy reel with a strong hook.",
        ],
        "long_form": [
            "Publish a step-by-step breakdown of your {niche} process from idea to result.",
            "Record a case study showing how you improved at one part of {niche} over time.",
            "Create a beginner guide covering the tools, habits, and milestones in {niche}.",
        ],
        "deep_dive": [
            "Build a multi-part series unpacking major trends shaping {niche} this year.",
            "Interview another creator in {niche} and compare your workflows, tools, and lessons.",
            "Create a deep analysis of what separates average {niche} content from memorable work.",
        ],
        "related_creators": [
            "{niche} Trend Watch",
            "{niche} Breakdown Lab",
            "{niche} Creator Spotlight",
        ],
    },
    "ai": {
        "short_form": [
            "Demo one prompt that saves creators 30 minutes and show the before/after output.",
            "Break down one AI tool in 25 seconds: what it does, who it helps, and one catch.",
            "React to a viral AI claim and explain whether it is actually useful for creators.",
        ],
        "long_form": [
            "Publish a workflow video showing how you use AI from research to final content.",
            "Compare three AI tools for the same creator task and rank them honestly.",
            "Walk through an automation build that solves one repetitive problem for creators.",
        ],
        "deep_dive": [
            "Create a long-form guide on prompt design for different creator niches.",
            "Break down embeddings, recommendations, and content ranking in plain English.",
            "Produce an opinionated essay on where AI helps creators and where it hurts trust.",
        ],
        "related_creators": [
            "AI Workflow Studio",
            "Prompt Systems Creator",
            "Automation Build Journal",
        ],
    },
    "fashion": {
        "short_form": [
            "Style one item three ways and frame it as a quick outfit challenge.",
            "Post a trend reaction reel explaining what you would actually wear and why.",
            "Film a fast thrift-to-lookbook transformation with text overlays for each piece.",
        ],
        "long_form": [
            "Create a seasonal capsule wardrobe guide for a specific lifestyle or budget.",
            "Break down how you plan, source, and style a full shoot from concept to final look.",
            "Record a fashion deep chat on trends worth trying versus trends to skip.",
        ],
        "deep_dive": [
            "Publish a detailed analysis of how color, fit, and silhouette change an outfit story.",
            "Document the business side of fashion content: sourcing, brand deals, and styling prep.",
            "Build a series exploring sustainable fashion choices without losing personal style.",
        ],
        "related_creators": [
            "Capsule Closet Creator",
            "Street Style Breakdown",
            "Editorial Lookbook Journal",
        ],
    },
    "beauty": {
        "short_form": [
            "Show one product test in real lighting with a quick honest verdict.",
            "Turn a common makeup mistake into a fast fix video with side-by-side results.",
            "Post a skincare routine reel built around one skin concern and one hero product.",
        ],
        "long_form": [
            "Film a full routine breakdown for a specific event, mood, or budget.",
            "Compare affordable and premium beauty products in one detailed review video.",
            "Create a tutorial explaining not just what to use, but why each step matters.",
        ],
        "deep_dive": [
            "Build an educational series on ingredient literacy and how to read product labels.",
            "Document how beauty trends move from runway or TikTok into everyday routines.",
            "Publish a long-form conversation on honest reviews, sponsorships, and audience trust.",
        ],
        "related_creators": [
            "Routine Reset Creator",
            "Ingredient Breakdown Studio",
            "Beauty Review Notes",
        ],
    },
    "fitness": {
        "short_form": [
            "Film one exercise form tip that instantly improves a common movement.",
            "Share a 30-second workout finisher people can save and try today.",
            "Turn a gym myth into a quick evidence-based creator take.",
        ],
        "long_form": [
            "Build a weekly training plan video for beginners with clear progression tips.",
            "Walk through a full workout and explain the purpose of each movement.",
            "Create a realistic nutrition and recovery guide for busy creators.",
        ],
        "deep_dive": [
            "Produce a deep series on strength, mobility, and recovery working together.",
            "Document your coaching philosophy and how you adapt plans for different goals.",
            "Compare popular fitness trends and explain which ones deliver real results.",
        ],
        "related_creators": [
            "Form Fix Coach",
            "Strength Progress Journal",
            "Recovery and Routine Lab",
        ],
    },
    "wellness": {
        "short_form": [
            "Share one calming habit that fits into a packed day in under two minutes.",
            "Make a quick reset reel for stressful mornings, afternoons, or evenings.",
            "Turn a simple mindset prompt into a saveable wellness check-in clip.",
        ],
        "long_form": [
            "Create a full routine video for better energy, focus, and recovery across the day.",
            "Document one week of wellness experiments and what actually helped.",
            "Break down a realistic self-care system that does not rely on expensive products.",
        ],
        "deep_dive": [
            "Produce a thoughtful series on burnout, boundaries, and sustainable creator routines.",
            "Explore how sleep, movement, food, and digital habits affect emotional wellbeing.",
            "Host a long-form conversation on what wellness content gets right and wrong online.",
        ],
        "related_creators": [
            "Mindful Routine Creator",
            "Wellbeing Reset Studio",
            "Balanced Living Notes",
        ],
    },
    "tech": {
        "short_form": [
            "Demo one underrated feature in a tool creators already use every day.",
            "Explain one piece of tech news in plain language and why creators should care.",
            "Post a fast side-by-side comparison of two tools solving the same problem.",
        ],
        "long_form": [
            "Create a practical review of a new creator tool after using it in a real workflow.",
            "Build a desk setup or creator stack walkthrough focused on productivity and tradeoffs.",
            "Walk through one technical topic slowly enough for non-technical creators to follow.",
        ],
        "deep_dive": [
            "Publish a long-form analysis of how creator tools shape output quality and speed.",
            "Compare ecosystems, lock-in, and pricing across the tools your audience uses most.",
            "Create a deep educational breakdown of one emerging technology trend for creators.",
        ],
        "related_creators": [
            "Tool Review Engineer",
            "Creator Stack Breakdown",
            "Plain English Tech Notes",
        ],
    },
    "gaming": {
        "short_form": [
            "Clip one clutch play with commentary on the decision that made it work.",
            "Turn one patch note into a fast reaction with real gameplay context.",
            "Post a quick challenge format your audience can try in the same game.",
        ],
        "long_form": [
            "Create a strategy guide for one map, role, build, or ranked scenario.",
            "Document the path from casual play to competitive improvement in one title.",
            "Build a review-style video on what makes a game worth sticking with long term.",
        ],
        "deep_dive": [
            "Produce a meta breakdown showing how balance changes affect player behavior.",
            "Create a long-form essay on storytelling, mechanics, or community culture in a game.",
            "Explore how creators can stand out in crowded gaming niches without clickbait.",
        ],
        "related_creators": [
            "Ranked Grind Creator",
            "Patch Note Analyst",
            "Lore and Mechanics Lab",
        ],
    },
    "finance": {
        "short_form": [
            "Explain one money concept creators confuse all the time in under 30 seconds.",
            "Break down one spending habit that quietly hurts new freelancers.",
            "Turn a finance headline into a fast creator-focused takeaway.",
        ],
        "long_form": [
            "Make a practical budgeting guide for creators with inconsistent income.",
            "Walk through how to price brand deals, products, or freelance offers with examples.",
            "Create a personal finance system video focused on cash flow, taxes, and savings.",
        ],
        "deep_dive": [
            "Build a deep series on financial habits that help creators stay in business longer.",
            "Explain tax planning, emergency funds, and revenue diversification for small creators.",
            "Publish a long-form breakdown of how money psychology affects creator decisions.",
        ],
        "related_creators": [
            "Creator Money Coach",
            "Freelance Finance Notes",
            "Cash Flow Breakdown",
        ],
    },
    "food": {
        "short_form": [
            "Film one recipe shortcut that makes a meal faster without ruining the result.",
            "Turn a pantry ingredient into a quick challenge-style cooking reel.",
            "Post a taste-test reaction with one useful takeaway people can use tonight.",
        ],
        "long_form": [
            "Create a full recipe video with prep, plating, and common mistakes to avoid.",
            "Build a weekly meal-prep system around one budget, diet, or time constraint.",
            "Document a cook-through where you improve a dish over three iterations.",
        ],
        "deep_dive": [
            "Produce a long-form food story connecting technique, culture, and ingredient choice.",
            "Explore how restaurant trends influence home cooking and creator food content.",
            "Create an educational breakdown of flavor building for beginners.",
        ],
        "related_creators": [
            "Home Kitchen Creator",
            "Flavor Breakdown Studio",
            "Recipe Iteration Journal",
        ],
    },
    "travel": {
        "short_form": [
            "Share one place-specific travel tip most guides miss.",
            "Turn one day of travel into a cinematic highlight with practical text tips.",
            "Post a fast budget breakdown for a memorable local experience.",
        ],
        "long_form": [
            "Create a full itinerary guide for a city, weekend, or niche travel style.",
            "Document how you plan routes, pack gear, and capture footage on the move.",
            "Make a realistic review of a destination from a creator perspective, not a tourist brochure.",
        ],
        "deep_dive": [
            "Build a long-form story around culture, logistics, and lessons from a single trip.",
            "Compare slow travel and fast travel for creators trying to produce meaningful work.",
            "Explore how to travel responsibly while still making compelling content.",
        ],
        "related_creators": [
            "City Guide Storyteller",
            "Slow Travel Creator",
            "Budget Adventure Journal",
        ],
    },
    "business": {
        "short_form": [
            "Share one growth lesson from a recent project, launch, or client conversation.",
            "Turn a business mistake into a quick lesson with a strong hook and takeaway.",
            "Post a fast pricing, sales, or productivity tip for creator-entrepreneurs.",
        ],
        "long_form": [
            "Break down how you built one offer, system, or audience funnel from scratch.",
            "Create a business case study focused on what worked, what failed, and why.",
            "Walk through a realistic weekly CEO routine for a small creator-led brand.",
        ],
        "deep_dive": [
            "Produce a long-form series on positioning, productizing skills, and sustainable growth.",
            "Explore how creators can turn audience trust into offers without becoming salesy.",
            "Analyze common online business advice and separate signal from noise.",
        ],
        "related_creators": [
            "Creator Operator",
            "Growth Systems Journal",
            "Audience to Offer Lab",
        ],
    },
}

PROMPT = """You are a content strategist helping creators grow.
Given a niche, produce three categories of ideas: short_form (snackable clips),
long_form (tutorials, discussions), and deep_dive (research or extended stories).
Respond with JSON: {"short_form":[...],"long_form":[...],"deep_dive":[...],"related_creators":[...]}"""


def _normalize_niche(niche: str) -> str:
    raw = niche.strip().lower()
    return NICHE_ALIASES.get(raw, raw)


def _format_ideas(ideas: list[str], niche: str) -> list[str]:
    label = niche.title() if niche else "Creator"
    return [idea.format(niche=label) for idea in ideas]


def _fallback(niche: str) -> ContentIdeas:
    normalized_niche = _normalize_niche(niche or "")
    label = normalized_niche or "default"
    template = IDEA_TEMPLATES.get(label, IDEA_TEMPLATES["default"])
    short = _format_ideas(template["short_form"], normalized_niche)
    long = _format_ideas(template["long_form"], normalized_niche)
    deep = _format_ideas(template["deep_dive"], normalized_niche)
    related = _format_ideas(template["related_creators"], normalized_niche)
    return ContentIdeas(
        short_form=short,
        long_form=long,
        deep_dive=deep,
        related_creators=related,
    )


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
