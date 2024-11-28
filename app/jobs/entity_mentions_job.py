import warnings
import ast

from redis.utils import from_url
from rq import Queue, Retry
from sqlalchemy.sql import text

from app.core.database import sessionmanager
from app.core.config import settings
from app.core.dependencies import get_ner_model, get_embedder
from app.models import EntityMention, Article
from app.services import NamedEntityLinker


warnings.filterwarnings("ignore", category=FutureWarning)

queue = Queue('entity-mentions', connection=from_url(settings.redis_url), default_timeout=settings.rq_timeout)

def enqueue_entity_mentions(article_id: str):
    return queue.enqueue_call(
        func=detect_entity_mentions,
        args=(article_id,),
        result_ttl=2000,
        retry=Retry(max=1)
    )

async def detect_entity_mentions(article_id: str):
    named_entity_linker = NamedEntityLinker()
    embedder = get_embedder()
    ner_model = get_ner_model()
    
    async with sessionmanager.session() as session:
        async with session.begin():
            article = await session.get(Article, article_id)
            detected_entities = ner_model.get_named_entities(article.article)

            entities = await get_entities(session, article_id)
            entity_names = [entity.name for entity in entities]
            matrix = [ast.literal_eval(entity.vector) for entity in entities]

            for detected_entity in detected_entities:
                embedding = embedder.get_embedding(detected_entity['name'])
                similarity, entity_idx = named_entity_linker.get_most_similar_entity(
                    vector=embedding,
                    matrix=matrix, 
                    name=detected_entity['name'], 
                    entity_names=entity_names
                )
                if similarity > settings.entity_similarity_threshold:
                    entity_mention = await create_entity_mention(
                        session, 
                        entities[entity_idx].id, 
                        article_id, detected_entity, 
                        embedding, 
                        similarity
                    )
            
            await session.commit()
    return {"article_id": article_id}

async def get_entities(session, article_id: str):
    query = text("""
        SELECT 
            entities.id, 
            entities.name, 
            entities.vector
        FROM 
            entities
        JOIN 
            article_entity_sentiment_topics 
            ON article_entity_sentiment_topics.entity_id = entities.id
        WHERE 
            article_entity_sentiment_topics.article_id = :article_id
        """
    )
    result = await session.execute(query, {"article_id": article_id})
    entities = result.fetchall()
    return entities

async def create_entity_mention(session, entity_id, article_id, detected_entity, embedding, similarity):
    entity_mention = EntityMention(
        article_id=article_id,
        entity_id=entity_id,
        name=detected_entity["name"],
        start_pos=detected_entity["start_pos"],
        end_pos=detected_entity["end_pos"],
        confidence=detected_entity["confidence"],
        type=detected_entity["type"],
        source="NER",
        vector=embedding,
        similarity=similarity
    )
    session.add(entity_mention)
    return entity_mention