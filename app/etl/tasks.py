from celery_app import celery_app
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Article, ArticleEntitySentimentTopic
from source.processors import Preprocessor, Translator

translator = Translator(from_code='de', to_code='en') 

@celery_app.task
def process_article_task(article: dict):
    db: Session = next(get_db())

    def map_triplet(triplet):
        entity_apa_id, topic_apa_id, sentiment_apa_id = triplet
        
        entity = db.query(Entity).filter(Entity.apa_id == entity_apa_id).first()
        topic = db.query(Topic).filter(Topic.apa_id == topic_apa_id).first()
        sentiment = db.query(Sentiment).filter(Sentiment.apa_id == sentiment_apa_id).first()
        
        return {
            "entity_id": entity.id if entity else None,
            "topic_id": topic.id if topic else None,
            "sentiment_id": sentiment.id if sentiment else None
        }

    try:
        text = Preprocessor.process_text(article["article"])
        title = Preprocessor.process_text(article["title"])
        sentiments = Preprocessor.process_sentiment(article["sentiments"])

        article_english = Article(
            apa_id=article["apa_id"],
            published_date=article["published_date"],
            title=translator.translate(title),
            article=translator.translate(text),
            language="ENG"
        )
        article_german = Article(
            apa_id=article["apa_id"],
            published_date=article["published_date"],
            title=title,
            article=text,
            language="GER"
        )
    
        db.add(article_english)
        db.add(article_german)
        await db.commit()
        db.refresh(article_english)

        triplets = Preprocessor.process_sentiment(article["sentiments"])

        db.add_all(ArticleEntitySentimentTopic(**map_triplet(triplet), article_id=article_english.id) 
            for triplet in triplets)
        await db.commit()
    
    except Exception as e:
        await db.rollback()
        raise e

        return {"status": "success", "apa_id": article["apa_id"]}

    except Exception as e:
        return {"status": "failed", "error": str(e)}
