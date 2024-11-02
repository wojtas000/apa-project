from pydantic import BaseModel
from enum import Enum


class EntityType(str, Enum):
    organization = "organization"
    person = "person"
    product = "product"

class EntityCreate(BaseModel):
    apa_id: str
    name: str
    type: EntityType
    source: str = "APA"

class TopicType(str, Enum):
    individual = "individual"
    standard = "standard"

class TopicCreate(BaseModel):
    apa_id: str
    name: str
    type: TopicType

class SentimentType(str, Enum):
    high = "high"
    low = "low"

class SentimentCreate(BaseModel):
    apa_id: str
    name: str
    type: SentimentType
