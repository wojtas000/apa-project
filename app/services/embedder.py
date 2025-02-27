import torch

from transformers import AutoTokenizer, AutoModel
from typing import List
from app.core.config import settings


class Embedder:
    def __init__(self, model_name: str = settings.embedding_model):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)


    def get_embedding(self, text: str) -> List[float]:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.squeeze().tolist()
