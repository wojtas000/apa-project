import uuid

from sqlalchemy import Column, String, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base
from app.core.config import settings


class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apa_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    type = Column(Enum("high", "low", name='sentiment_type_enum'), nullable=True)
    vector = Column(Vector(settings.embedding_size), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    article_entity_sentiment_topics = relationship("ArticleEntitySentimentTopic", back_populates="sentiment")
