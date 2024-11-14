from pydantic import BaseModel
from enum import Enum


class TopicType(str, Enum):
    individual = "individual"
    standard = "standard"

class TopicCreate(BaseModel):
    apa_id: str
    name: str
    type: TopicType