import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, CHAR, DateTime, func, Text, JSON, Enum
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator

from app.config import settings

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apa_coding = Column(String, nullable=False)
    title_english = Column(String, nullable=True)
    article_english = Column(Text, nullable=True)
    title_german = Column(String, nullable=True)
    article_german = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Entity(Base):
    __tablename__ = "entities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apa_coding = Column(String, nullable=True)
    name = Column(String, nullable=False)
    source = Column(Enum("APA", "NER", name='entity_source_enum'), nullable=False)
    vector = Column(Vector(512), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class EntityMention(Base):
    __tablename__ = "entity_mentions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False)
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    confidence = Column(Integer, nullable=True)
    source = Column(Enum("APA", "NER", name='entity_mention_source_enum'), nullable=False)
    type = Column(Enum("ORG", "PER", "LOC", "MISC", name='entity_mention_type_enum'), nullable=False)
    vector = Column(Vector(512), nullable=True)

    entity = relationship("Entity", back_populates="entity_mentions")
    article = relationship("Article", back_populates="entity_mentions")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apa_coding = Column(String, nullable=True)
    name = Column(String, nullable=False)
    vector = Column(Vector(512), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Sentiment(Base):
    __tablename__ = "sentiments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apa_coding = Column(String, nullable=True)
    name = Column(String, nullable=False)
    vector = Column(Vector(512), nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class ArticleEntitySentimentTopic(Base):
    __tablename__ = "article_entity_sentiment_aspects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"), nullable=False)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("entities.id"), nullable=False)
    sentiment_id = Column(UUID(as_uuid=True), ForeignKey("sentiments.id"), nullable=False)
    topic_id = Column(String, nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"), nullable=False)

    article = relationship("Article", back_populates="article_entity_sentiment_aspects")
    entity = relationship("Entity", back_populates="article_entity_sentiment_aspects")
    sentiment = relationship("Sentiment", back_populates="article_entity_sentiment_aspects")
    topic = relationship("Topic", back_populates="article_entity_sentiment_aspects")
    model = relationship("Model", back_populates="article_entity_sentiment_aspects")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Model(Base):
    __tablename__ = "models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    type = Column(Enum("NER", "ABSA", "TABSA", name='model_types_enum'), nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
