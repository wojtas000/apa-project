import uuid

from sqlalchemy import Column, String, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base
from app.core.config import settings

class Entity(Base):
    __tablename__ = "entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apa_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    source = Column(Enum("APA", "NER", name='entity_source_enum'), nullable=False)
    type = Column(Enum("organization", "person", "product", name='entity_type_enum'), nullable=True)
    vector = Column(Vector(settings.embedding_size), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    entity_mentions = relationship("EntityMention", back_populates="entity")
    article_entity_sentiment_topics = relationship("ArticleEntitySentimentTopic", back_populates="entity")
