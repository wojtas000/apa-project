from pydantic import BaseModel
from enum import Enum


class SentimentType(str, Enum):
    high = "high"
    low = "low"

class SentimentCreate(BaseModel):
    apa_id: str
    name: str
    type: SentimentType
