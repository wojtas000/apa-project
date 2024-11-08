# Run server
```
uvicorn --reload --port 8000 app.main:app
```

# Start celery worker
```
PYTHONPATH=./app celery -A app.celery_app.celery_app worker --loglevel=info
```

# Start flower for background task monitoring
```
celery -A app.celery_app.celery_app flower
```