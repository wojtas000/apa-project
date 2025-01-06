from .article import router as article_router
from .etl import router as etl_router
from .inference import router as inference_router
from .train import router as train_router

__all__ = [
    "article_router",
    "etl_router",
    "inference_router", 
    "train_router"
]
