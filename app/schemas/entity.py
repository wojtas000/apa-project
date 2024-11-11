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