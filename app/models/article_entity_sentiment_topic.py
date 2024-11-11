import uuid
from sqlalchemy import Column, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

class ArticleEntitySentimentTopic(Base):
    __tablename__ = "article_entity_sentiment_topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    sentiment_id = Column(UUID(as_uuid=True), ForeignKey("sentiments.id"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=True)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"), nullable=True)

    article = relationship("Article", back_populates="article_entity_sentiment_topics")
    entity = relationship("Entity", back_populates="article_entity_sentiment_topics")
    sentiment = relationship("Sentiment", back_populates="article_entity_sentiment_topics")
    topic = relationship("Topic", back_populates="article_entity_sentiment_topics")
    model = relationship("Model", back_populates="article_entity_sentiment_topics")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
