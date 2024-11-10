import uuid

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from celery.result import AsyncResult
from app.config import settings
from app.database import get_db
from app.auth import api_key_auth
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Entity, Topic, Sentiment, Article
from app.etl.schemas import EntityCreate, TopicCreate, SentimentCreate
from app.etl.service import generate_articles
from app.etl import tasks
from source.embedder import Embedder
from source.processors import Translator, Preprocessor


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

    article_generator = generate_articles(await file.read())
    for article in article_generator:
        task = tasks.enqueue_article_load(article)
        
    return {
        "job_id": job_id,
        "message": "File processing started in background"
        }

# @router.post("/articles")
# async def create_article(article: Article, db: AsyncSession = Depends(get_db), response_model_exclude_none=True):
#     try:
#         db_article = ArticleModel(**article.dict())
#         db.add(db_article)
#         db.commit()
#         db.refresh(db_article)
#         return db_article
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(e))
