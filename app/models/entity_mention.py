import uuid

from sqlalchemy import Column, String, Integer, Float, Enum, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.core.database import Base
from app.core.config import settings

class EntityMention(Base):
    __tablename__ = "entity_mentions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False)
    name = Column(String, nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    confidence = Column(Float, nullable=False)
    source = Column(Enum("APA", "NER", name='entity_mention_source_enum'), nullable=False)
    type = Column(Enum("ORG", "PER", "LOC", "MISC", name='entity_mention_type_enum'), nullable=False)
    vector = Column(Vector(settings.embedding_size), nullable=True)
    similarity = Column(Float, nullable=True)

    entity = relationship("Entity", back_populates="entity_mentions")
    article = relationship("Article", back_populates="entity_mentions")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
