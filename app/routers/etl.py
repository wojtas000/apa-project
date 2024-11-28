import uuid

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import api_key_auth
from app.core.dependencies import get_embedder
from app.models import Entity, Topic, Sentiment
from app.schemas import EntityCreate, TopicCreate, SentimentCreate
from app.jobs.load_article_job import enqueue_load_article
from app.services import Embedder, ArticleGenerator


router = APIRouter(prefix="/etl", tags=["etl"])

@router.post(
    "/entity", 
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def create_entity(data: EntityCreate, db: AsyncSession = Depends(get_db), embedder: Embedder = Depends(get_embedder)):
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
async def create_topic(data: TopicCreate, db: AsyncSession = Depends(get_db), embedder: Embedder = Depends(get_embedder)):
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
async def create_sentiment(data: SentimentCreate, db: AsyncSession = Depends(get_db), embedder: Embedder = Depends(get_embedder)):
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

@router.get(
    "/entity/{entity_id}",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_entity_mentions(entity_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    entity = await db.get(Entity, entity_id)
    return {"entity": entity.name}
