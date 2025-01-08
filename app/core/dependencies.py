from app.services import Embedder, NERModel
from fastapi import Request

def get_ner_model(request: Request):
    return NERModel(tagger=request.app.state.models["ner"])

def get_sentiment_classifier(request: Request):
    return request.app.state.models["sentiment_classifier"]

def get_embedder():
    return Embedder()
