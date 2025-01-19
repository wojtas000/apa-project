import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from rq_dashboard_fast import RedisQueueDashboard
from flair.models import SequenceTagger

from app.core.config import settings
from app.routers import *
from app.admin import init_admin
from app.services import Translator

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from pyabsa import AspectPolarityClassification as APC

    app.state.models = {}
    app.state.models["ner"] = SequenceTagger.load("flair/ner-english")
    app.state.models["sentiment_classifier"] = APC.SentimentClassifier(
        checkpoint=settings.sentiment_classifier_checkpoint
    )
    
    yield

    for model in app.state.models.values():
        del model
    app.state.models.clear()

app = FastAPI(lifespan=lifespan)

# postgres
init_admin(app)

# redis
rq_dashboard = RedisQueueDashboard(
    redis_url=settings.redis_url, 
    prefix="/rq"
    )

app.mount("/rq", rq_dashboard)

# mlflow
@app.get("/mlflow")
async def redirect_mlflow():
    return RedirectResponse(url=settings.mlflow_tracking_uri)

# minio
@app.get("/minio")
async def redirect_minio():
    return RedirectResponse(url=settings.minio_frontend)

@app.get("/")
async def redirect_docs():
    return RedirectResponse(url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(article_router)
app.include_router(etl_router)
app.include_router(inference_router)
app.include_router(train_router)
app.include_router(dataset_router)
