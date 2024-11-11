import uuid
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apa_id = Column(String, nullable=False)
    title= Column(String, nullable=True)
    article = Column(Text, nullable=True)
    language = Column(String(3), nullable=True)
    published_date = Column(DateTime, nullable=True)


    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    entity_mentions = relationship("EntityMention", back_populates="article")
    article_entity_sentiment_topics = relationship("ArticleEntitySentimentTopic", back_populates="article")
