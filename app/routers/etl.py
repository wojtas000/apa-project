import uuid

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.config import settings
from app.core.database import get_db
from app.core.auth import api_key_auth
from app.core.dependencies import get_ner_model
from app.models import Entity, Topic, Sentiment, Article
from app.schemas import EntityCreate, TopicCreate, SentimentCreate, EntityMentionsDetect
from app.jobs.load_article_job import enqueue_load_article 
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
    "/detect_entity_mentions",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def detect_entity_mentions(data: EntityMentionsDetect, ner_model = Depends(get_ner_model), db: AsyncSession = Depends(get_db)):
    predictions = ner_model.get_named_entities(data.text)
    embeddings = [embedder.get_embedding(prediction["name"]) for prediction in predictions] 

    preds = []

    for embedding in embeddings:
        embedding_vector = query_embedding_str = ",".join(map(str, embedding))
        
        query = text("""
            SELECT id, name, 1 - (vector <-> :embedding) AS similarity
            FROM entities
            ORDER BY vector <-> :embedding
            LIMIT 1
        """)
        result = await db.execute(query, {"embedding": embedding_vector})
        most_similar_entity = result.fetchone()

        preds.append({
            "entity_id": most_similar_entity.id,
            "name": most_similar_entity.name,
            "similarity": most_similar_entity.similarity
        })

    return {"predictions": preds}

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
