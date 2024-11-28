from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.models.article import Article
from app.repositories.base_repository import BaseRepository


class ArticleRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Article)

    async def get_article_triplets(self, id: str):
        query = text(
            """
            SELECT 
                entities.name AS entity_name, 
                sentiments.name AS sentiment_name, 
                topics.name AS topic_name
            FROM 
                article_entity_sentiment_topics
            JOIN 
                entities 
                ON article_entity_sentiment_topics.entity_id = entities.id
            JOIN 
                sentiments 
                ON article_entity_sentiment_topics.sentiment_id = sentiments.id
            LEFT JOIN 
                topics 
                ON article_entity_sentiment_topics.topic_id = topics.id
            WHERE 
                article_entity_sentiment_topics.article_id = :article_id
            """
        )
        rows = await self.db.execute(query, {"article_id": id})
        return rows.all()

    async def get_training_data(self, id: str):
        query = text(
        """
        SELECT 
            em.*, 
            s.name AS sentiment_name, 
            a.article AS article_text,
            e.name AS entity_name
        FROM 
            entity_mentions em
        JOIN 
            article_entity_sentiment_topics aes 
            ON em.article_id = aes.article_id AND em.entity_id = aes.entity_id
        JOIN 
            sentiments s 
            ON aes.sentiment_id = s.id
        JOIN 
            articles a 
            ON em.article_id = a.id
        JOIN entities e ON em.entity_id = e.id
        WHERE 
            em.article_id = :article_id AND aes.topic_id IS NULL
        """
    )

        rows = await self.db.execute(query, {"article_id": id})
        return rows.all()