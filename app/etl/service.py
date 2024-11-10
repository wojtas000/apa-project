from typing import Generator, Dict
import xml.etree.ElementTree as ET
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Article, ArticleEntitySentimentTopic
from source.processors import Preprocessor, Translator

def generate_articles(data) -> Generator[Dict[str, str], None, None]:
    root = ET.fromstring(data)
    
    for document in root.findall('.//Document'):
        doc_id = document.get('id')
        published_date = document.find('.//DOC').get('TIMESTAMP')
        title = document.find(".//FELD[@NAME='TITEL']")
        article = document.find(".//FELD[@NAME='INHALT']")
        sentiments = document.find(".//FELD[@NAME='EVALUATIONS']")
        try:
            yield {
                "apa_id": doc_id,
                "published_date": published_date,
                "title": ET.tostring(title, encoding='unicode', method='text'),
                "article": ET.tostring(article, encoding='unicode', method='text'),
                "sentiments": ET.tostring(sentiments, encoding='unicode', method='text'),
            }
        except:
            continue

def process_article(
    article: Dict,
    db: AsyncSession,
):
    text = Preprocessor.process_text(article["article"])
    title = Preprocessor.process_text(article["title"])
    sentiments = Preprocessor.process_sentiment(article["sentiments"])

    article_english = Article(
        apa_id=article["apa_id"],
        published_date=article["published_date"],
        title=Translator.translate(article["title"]),
        article=Translator.translate(article["article"]),
        language="ENG"
    )

    article_german = Article(
        apa_id=article["apa_id"],
        published_date=article["published_date"],
        title=article["title"],
        article=article["article"],
        language="GER"
    )


    db.add(article_english)
    db.add(article_german)
    db.add_all(ArticleEntitySentimentTopic(**sentiment) for sentiment in sentiments)
    db.commit()