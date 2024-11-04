from celery import Celery

celery_app = Celery(
    "background_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

celery_app.conf.update(
    result_expires=3600,
)
