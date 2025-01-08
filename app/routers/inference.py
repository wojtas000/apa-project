from fastapi import APIRouter, Depends

from app.core.dependencies import get_sentiment_classifier
from app.schemas.inference import InferenceInput

router = APIRouter(prefix="/inference", tags=["inference"])


@router.post(
    "",
    response_model_exclude_none=True
)
async def predict(data: InferenceInput, sentiment_classifier=Depends(get_sentiment_classifier)):
    prediction = sentiment_classifier.predict(data.text)
    return {
        'text': prediction['text'],
        'aspect': prediction['aspect'][0],
        'sentiment': prediction['sentiment'][0],
        'confidence': prediction['confidence'][0],
    }

def process_output(x):
    probs = {
    'negative': x['probs'][0],
    'neutral': x['probs'][1],
    'positive': x['probs'][2]
    }
    return {
        'text': x['text'],
        'aspect': x['aspect'][0],
        'sentiment': x['sentiment'][0].lower(),
        'confidence': x['confidence'][0],
        'probs': probs
    }