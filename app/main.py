import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from rq_dashboard_fast import RedisQueueDashboard
from flair.models import SequenceTagger

from app.core.config import settings
from app.core.database import sessionmanager
from app.routers import *
from app.admin import init_admin
from app.services import Translator, NERModel

logging.basicConfig(level=logging.DEBUG)

models = {}
models["ner"] = SequenceTagger.load("flair/ner-english")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Translator.install_package(from_code='de', to_code='en')
    yield

app = FastAPI(lifespan=lifespan)
init_admin(app)

rq_dashboard = RedisQueueDashboard(
    redis_url=settings.redis_url, 
    prefix="/rq"
    )

app.mount("/rq", rq_dashboard)

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
app.include_router(training_router)
