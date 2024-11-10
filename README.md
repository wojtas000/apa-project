# Run server
```
uvicorn --reload --port 8000 app.main:app
```

# Start celery worker
```
celery -A app.celery_app.celery_app worker --loglevel=info --concurrency=4

```

# Start flower for background task monitoring
```
celery -A app.celery_app.celery_app flower
```