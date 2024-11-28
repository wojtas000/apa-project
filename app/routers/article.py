import uuid
from collections import defaultdict
from functools import reduce

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import api_key_auth
from app.repositories import ArticleRepository
from app.jobs.entity_mentions_job import enqueue_entity_mentions
from app.services import ArticleService

router = APIRouter(prefix="/article", tags=["article"])


@router.post(
    "/{article_id}/entity_mentions",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def detect_entity_mentions(
    article_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    enqueue_entity_mentions(article_id)
    return {"message": "Entity mentions detection started in background", "article_id": article_id}

@router.get(
    "/{article_id}",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_article(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    article_repo = ArticleRepository(db)
    article = await article_repo.get_by_id(article_id)
    return {"article": article}

@router.get(
    "",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_articles(db: AsyncSession = Depends(get_db)):
    article_repo = ArticleRepository(db)
    articles = await article_repo.get_all()
    return {"articles": articles}

@router.get(
    "/{article_id}/triplets",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_article_triplets(
    article_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db)
):
    article_repo = ArticleRepository(db)
    rows = await article_repo.get_article_triplets(article_id)
    article_entity_sentiment_topics = [
        {"entity": row.entity_name, "sentiment": row.sentiment_name, "topic": row.topic_name}
        for row in rows
    ]

    return {"article_entity_sentiment_topics": article_entity_sentiment_topics}

@router.get(
"/{article_id}/training_data",
dependencies=[Depends(api_key_auth)],
response_model_exclude_none=True
)
async def get_training_data(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await ArticleService(db=db).get_training_data(article_id)
