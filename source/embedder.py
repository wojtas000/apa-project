from transformers import AutoTokenizer, AutoModel
from app.config import settings
import torch
import torch.nn.functional as F

class Embedder:
    def __init__(self, model_name: str = settings.embedding_model):

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)


    def get_embedding(self, text: str) -> torch.Tensor:
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return list(embeddings.squeeze())
