import asyncio
from redis.utils import from_url
from rq import Queue, Retry, get_current_job
from rq.job import Job
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import sessionmanager
from app.models import Article, ArticleEntitySentimentTopic, Entity, Sentiment, Topic
from app.config import settings
from app.etl.preprocessor import Preprocessor
from app.etl.translator import Translator
from app.utils.decorators import timeit
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

translator = Translator(from_code='de', to_code='en') 
preprocessor = Preprocessor()
queue = Queue('load-xml', connection=from_url(settings.redis_url), default_timeout=settings.rq_timeout)


def enqueue_article_load(article: Dict):
    return queue.enqueue_call(
        func=task,
        args=(article,),
        result_ttl=2000,
        retry=Retry(max=1)
    )

@timeit
async def task(article: dict):
    async with sessionmanager.session() as session:
        async with session.begin():
            article_english_id = await create_article(session, article)

            triplets = preprocessor.process_sentiment(article["sentiments"])
            for triplet in triplets:
                processed_triplet = await process_triplet(session, triplet)
                if processed_triplet["entity_id"] and processed_triplet["sentiment_id"]:
                    article_entity_sentiment_topic = ArticleEntitySentimentTopic(**processed_triplet, article_id=article_english_id)
                    session.add(article_entity_sentiment_topic)

            return {"status": "success", "apa_id": article["apa_id"]}

@timeit
async def process_triplet(session, triplet):
        entity_apa_id, topic_apa_id, sentiment_apa_id = triplet
        
        entity = await session.execute(select(Entity).filter(Entity.apa_id == entity_apa_id))
        topic = await session.execute(select(Topic).filter(Topic.apa_id == topic_apa_id))
        sentiment = await session.execute(select(Sentiment).filter(Sentiment.apa_id == sentiment_apa_id))
        
        entity = entity.scalars().first()
        topic = topic.scalars().first()
        sentiment = sentiment.scalars().first()

        return {
            "entity_id": entity.id if entity else None,
            "topic_id": topic.id if topic else None,
            "sentiment_id": sentiment.id if sentiment else None
        }

@timeit
async def create_article(session, article):
    text = preprocessor.process_text(article["article"])
    title = preprocessor.process_text(article["title"])
    date = preprocessor.fix_date(article["published_date"])
    article_english = Article(
        apa_id=article["apa_id"],
        published_date=date,
        title=preprocessor.fix_punctuation(translator.translate(title)),
        article=preprocessor.fix_punctuation(translator.translate(text)),
        language="ENG"
    )
    article_german = Article(
        apa_id=article["apa_id"],
        published_date=date,
        title=title,
        article=text,
        language="GER"
    )

    session.add(article_english)
    session.add(article_german)
    await session.flush()
    return article_english.id
