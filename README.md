# Run server
```
uvicorn --reload --port 8000 app.main:app
```

# Start celery worker
```
celery -A celery_app.celery_app worker --loglevel=info
```

# Start flower for background task monitoring
```
celery -A celery_app.celery_app flower
```