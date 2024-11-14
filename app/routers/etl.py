import uuid
import logging
import ast

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db
from app.core.auth import api_key_auth
from app.core.dependencies import get_ner_model
from app.models import Entity, Topic, Sentiment, Article, EntityMention
from app.schemas import EntityCreate, TopicCreate, SentimentCreate, EntityMentionsDetect
from app.jobs.load_article_job import enqueue_load_article
from app.jobs.entity_mentions_job import enqueue_entity_mentions 
from app.services import Embedder, Preprocessor, Translator, ArticleGenerator


router = APIRouter(prefix="/etl", tags=["etl"])

embedder = Embedder()

@router.post(
    "/entity", 
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def create_entity(data: EntityCreate, db: AsyncSession = Depends(get_db)):
    entity = Entity(
        apa_id=data.apa_id,
        name=data.name,
        source=data.source,
        vector = embedder.get_embedding(data.name),
        type=data.type
    )
    try:
        db.add(entity)
        await db.commit()
        return await db.refresh(entity)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create entity: {e}"
        )

@router.post(
    "/topic",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def create_topic(data: TopicCreate, db: AsyncSession = Depends(get_db)):
    topic = Topic(name=data.name, apa_id=data.apa_id, vector=embedder.get_embedding(data.name), type=data.type)
    db.add(topic)
    try:
        await db.commit()
        return await db.refresh(topic)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create topic: {e}"
        )

@router.post(
    "/sentiment",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def create_sentiment(data: SentimentCreate, db: AsyncSession = Depends(get_db)):
    sentiment = Sentiment(name=data.name, apa_id=data.apa_id, vector=embedder.get_embedding(data.name), type=data.type)
    db.add(sentiment)
    try:
        await db.commit()
        return await db.refresh(sentiment)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create sentiment: {e}"
        )

@router.post(
    "/xml",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def import_xml_articles(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith('.xml'):
        raise HTTPException(status_code=400, detail="File must be XML")

    job_id = str(uuid.uuid4())

    article_generator = ArticleGenerator.generate_articles(await file.read())
    for article in article_generator:
        task = enqueue_load_article(article)
        
    return {
        "job_id": job_id,
        "message": "File processing started in background"
        }

@router.post(
    "/article/{article_id}/entity_mentions",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def detect_entity_mentions(
    article_id: uuid.UUID, 
    # ner_model = Depends(get_ner_model), 
    db: AsyncSession = Depends(get_db)
):
    enqueue_entity_mentions(article_id)
    return {"message": "Entity mentions detection started in background", "article_id": article_id}

@router.get(
    "/article/{article_id}",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_entity_mentions(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    article = await db.get(Article, article_id)
    return {"article": article}

@router.get(
    "/entity/{entity_id}",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_entity_mentions(entity_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    entity = await db.get(Entity, entity_id)
    return {"entity": entity.name}

@router.get(
    "/article/{article_id}/triplets",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_article_triplets(
    article_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db)
):
    query = text(
        """
        SELECT entities.name AS entity_name, sentiments.name AS sentiment_name, topics.name AS topic_name
        FROM article_entity_sentiment_topics
        JOIN entities ON article_entity_sentiment_topics.entity_id = entities.id
        JOIN sentiments ON article_entity_sentiment_topics.sentiment_id = sentiments.id
        LEFT JOIN topics ON article_entity_sentiment_topics.topic_id = topics.id
        WHERE article_entity_sentiment_topics.article_id = :article_id
        """
    )

    # Fetch all results
    rows = await db.execute(query, {"article_id": article_id})

    # Format the results as a list of dictionaries
    article_entity_sentiment_topics = [
        {"entity": row.entity_name, "sentiment": row.sentiment_name, "topic": row.topic_name}
        for row in rows
    ]

    return {"article_entity_sentiment_topics": article_entity_sentiment_topics}

    