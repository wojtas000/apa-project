import uuid
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from app.core.database import get_db
from app.core.auth import api_key_auth
from app.core.config import settings
from app.repositories import ArticleRepository
from app.jobs.entity_mentions_job import enqueue_entity_mentions
from app.services import ArticleService
from app.schemas.article import TrainTestDevSplit

router = APIRouter(prefix="/article", tags=["article"])


@router.post(
    "/train_test_dev_split",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_train_test_dev_split(
    data: TrainTestDevSplit, 
    db: AsyncSession = Depends(get_db)
):

    dataset_name = data.dataset_name
    with_ambivalent = data.with_ambivalent

    dataset_path = Path(settings.app_root) / "intergrated_datasets/apc" / dataset_name 

    if not dataset_path.exists():
        dataset_path.mkdir(parents=True, exist_ok=True)
        train_file_path = dataset_path / f"{dataset_name}.train.dat.apc"
        test_file_path = dataset_path / f"{dataset_name}.test.dat.apc"
        dev_file_path = dataset_path / f"{dataset_name}.valid.dat.apc"
    else:
        raise HTTPException(status_code=400, detail="The provided dataset path already exists.")

    train, test, dev = await ArticleRepository(db).get_train_test_dev_split()
    with open(train_file_path, "w") as train_file, \
         open(test_file_path, "w") as test_file, \
         open(dev_file_path, "w") as dev_file:

        for dataset, file in zip([train, test, dev], [train_file, test_file, dev_file]):
            for row in dataset:
                training_data = await ArticleService(db).get_training_data(row.id, with_ambivalent=with_ambivalent)
                
                for data_row in training_data['training_data']:
                    file.write(f"{data_row['text']}\n")
                    file.write(f"{data_row['entity_name']}\n")
                    file.write(f"{data_row['sentiment']}\n")

    return {
        "train_path": train_file_path, 
        "test_path": test_file_path, 
        "dev_path": dev_file_path
    }  


@router.post(
    "/{article_id}/entity_mentions",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def detect_entity_mentions(
    article_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    enqueue_entity_mentions(article_id)
    return {"message": "Entity mentions detection started in background", "article_id": article_id}

@router.get(
    "/{article_id}",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_article(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    article_repo = ArticleRepository(db)
    article = await article_repo.get_by_id(article_id)
    return {"article": article}

@router.get(
    "/",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_articles(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    language: Optional[str] = None
):
    article_repo = ArticleRepository(db)
    articles = await article_repo.get_all(page, page_size, language)
    return {"articles": articles}

@router.get(
    "/{article_id}/triplets",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_article_triplets(
    article_id: uuid.UUID, 
    db: AsyncSession = Depends(get_db)
):
    article_repo = ArticleRepository(db)
    rows = await article_repo.get_article_triplets(article_id)
    article_entity_sentiment_topics = [
        {"entity": row.entity_name, "sentiment": row.sentiment_name, "topic": row.topic_name}
        for row in rows
    ]

    return {"article_entity_sentiment_topics": article_entity_sentiment_topics}

@router.get(
    "/{article_id}/training_data",
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
async def get_training_data(article_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await ArticleService(db=db).get_training_data(article_id)
