from .article import router as article_router
from .etl import router as etl_router
from .inference import router as inference_router
from .training import router as training_router

__all__ = [
    "article_router",
    "etl_router",
    "inference_router", 
    "training_router"
]
