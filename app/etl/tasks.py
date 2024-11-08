import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from celery.app import Celery
from app.celery_app import celery_app
from app.database import sessionmanager
from app.models import Article, ArticleEntitySentimentTopic, Entity, Sentiment, Topic
from app.config import settings
from app.etl.preprocessor import Preprocessor
from app.etl.translator import Translator


translator = Translator(from_code='de', to_code='en') 
preprocessor = Preprocessor()

@celery_app.task
def process_article_task(article: dict):
    asyncio.run(_process_article_task_async(article))


async def _process_article_task_async(article: dict):
    async with sessionmanager.session() as session:
        text = preprocessor.process_text(article["article"])
        title = preprocessor.process_text(article["title"])
        sentiments = preprocessor.process_sentiment(article["sentiments"])
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
        await session.commit()
        await session.refresh(article_english)

        triplets = preprocessor.process_sentiment(article["sentiments"])
        for triplet in triplets:
            processed_triplet = await process_triplet(session, triplet)
            if processed_triplet["entity_id"] is None or processed_triplet["sentiment_id"] is None:
                continue
            else:
                x = ArticleEntitySentimentTopic(**processed_triplet, article_id=article_english.id)
                session.add(x)
        await session.commit()

        return {"status": "success", "apa_id": article["apa_id"]}

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