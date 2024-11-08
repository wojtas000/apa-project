from celery import Celery
from app.config import settings

celery_app = Celery(
    "background_tasks",
    broker=settings.redis_url,
    backend=settings.redis_url
)
celery_app.autodiscover_tasks(['app.etl.tasks'])
celery_app.conf.update(
    result_expires=3600,
)
