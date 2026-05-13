from datetime import datetime, timedelta
from typing import Dict, List

from airflow import DAG
from airflow.operators.python import PythonOperator

from core.config import settings
from app.db.database import SessionLocal
from app.db.models.recommendations import Recommendation
from app.db.models.users import User
from app.services.embeddings import cosine_similarity, create_embedding
from app.services.llm import ContentIdeas, generate_content_ideas


DEFAULT_ARGS = {
    "owner": "creator-link-ai",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "retries": 0,
    "retry_delay": timedelta(minutes=1),
}


def _session():
    return SessionLocal()


def load_users(**kwargs):
    session = _session()
    users = session.query(User).all()
    session.close()
    kwargs["ti"].xcom_push(key="user_ids", value=[user.id for user in users])


def generate_embeddings(**kwargs):
    session = _session()
    users = session.query(User).all()
    for user in users:
        if not user.embedding:
            user.embedding = create_embedding(user.niche or "general")
    session.commit()
    session.close()


def compute_similar_similar(**kwargs):
    session = _session()
    users = session.query(User).filter(User.embedding != None).all()
    similar_map: Dict[int, List[str]] = {}
    for user in users:
        candidates = []
        for peer in users:
            if peer.id == user.id or not peer.embedding:
                continue
            score = cosine_similarity(user.embedding, peer.embedding)
            candidates.append((score, f"{peer.userName} · {peer.niche}"))
        candidates.sort(reverse=True)
        similar_map[user.id] = [name for _, name in candidates[:5]]
    session.close()
    kwargs["ti"].xcom_push(key="similar_map", value=similar_map)


def generate_ai_ideas(**kwargs):
    session = _session()
    users = session.query(User).all()
    ideas_map: Dict[int, ContentIdeas] = {}
    for user in users:
        ideas = generate_content_ideas(user.niche)
        ideas_map[user.id] = ideas
    session.close()
    kwargs["ti"].xcom_push(key="ideas_map", value=ideas_map)


def store_recommendations(**kwargs):
    session = _session()
    similar_map = kwargs["ti"].xcom_pull(key="similar_map") or {}
    ideas_map = kwargs["ti"].xcom_pull(key="ideas_map") or {}
    users = session.query(User).all()
    for user in users:
        ideas: ContentIdeas = ideas_map.get(user.id) or ContentIdeas([], [], [], [])
        similar = similar_map.get(user.id, [])
        rec = (
            session.query(Recommendation)
            .filter(Recommendation.creator_id == user.id)
            .one_or_none()
        )
        payload = {
            "short_form": ideas.short_form,
            "long_form": ideas.long_form,
            "deep_dive": ideas.deep_dive,
            "similar_creators": similar,
        }
        if not rec:
            rec = Recommendation(
                creator_id=user.id,
                niche=user.niche,
                **payload,
            )
            session.add(rec)
        else:
            rec.niche = user.niche
            rec.short_form = payload["short_form"]
            rec.long_form = payload["long_form"]
            rec.deep_dive = payload["deep_dive"]
            rec.similar_creators = payload["similar_creators"]
    session.commit()
    session.close()


with DAG(
    dag_id="creator_recommendations",
    schedule_interval="@daily",
    default_args=DEFAULT_ARGS,
    catchup=False,
) as dag:
    task_load_users = PythonOperator(
        task_id="load_users", python_callable=load_users, provide_context=True
    )
    task_embeddings = PythonOperator(
        task_id="generate_embeddings", python_callable=generate_embeddings
    )
    task_similarity = PythonOperator(
        task_id="compute_similarity", python_callable=compute_similar_similar, provide_context=True
    )
    task_ai_ideas = PythonOperator(
        task_id="generate_ai_ideas", python_callable=generate_ai_ideas, provide_context=True
    )
    task_store = PythonOperator(
        task_id="store_recommendations", python_callable=store_recommendations, provide_context=True
    )

    task_load_users >> task_embeddings >> task_similarity >> task_ai_ideas >> task_store
