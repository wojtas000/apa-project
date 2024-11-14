from pydantic import BaseModel


class EntityMentionsDetect(BaseModel):
    text: str