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
    probs = prediction['probs'][0].tolist()
    return {
        'text': prediction['text'],
        'aspect': prediction['aspect'][0],
        'sentiment': prediction['sentiment'][0],
        'confidence': prediction['confidence'][0],
        'probs': {
            'negative': probs[0],
            'neutral': probs[1],
            'positive': probs[2]
        }

    }
