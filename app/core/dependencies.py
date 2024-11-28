from app.services import Embedder, NERModel
from app import models

def get_ner_model():
    return NERModel(tagger=models["ner"])

def get_embedder():
    return Embedder()