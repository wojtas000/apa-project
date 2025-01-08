from pydantic import BaseModel

class InferenceInput(BaseModel):
    text: str
