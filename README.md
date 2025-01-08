# Actor-based sentiment analysis in press news articles

## System design
![Diagram](resources/diagram.png)

## Quickstart
1. Install packages with
```
pip install -r requirements.txt
```
2. Copy `.env.example` into `.env` and fill the required environmental variables
3. Start fastAPI server by running
```
fastapi run --reload app/main.py
```
alternatively
```
uvicorn app.main:app --reload --reload-dir=app --host=0.0.0.0 --port=8000
```

4. Start redis worker for background task processing with
```
python -m scripts.start_worker

```
5. Background task monitoring at `localhost:8000/rq/`
6. Admin panel at `localhost:8000/admin/`
7. Database backup:
```
docker exec -t <container-id> pg_dump -U postgres postgres > backups/backup.sql
```
8. Database migrations:
```
alembic revision --autogenerate -m "your_migration_message"
alembic upgrade head
```
9. Create requirements.txt (lockfile with all dependencies)
```bash
pip-compile -v --resolver=backtracking requirements.in --output-file requirements.txt
```
10. MLFlow
```bash
mlflow ui   --backend-store-uri postgresql://mlflow_user:mlflow_password@localhost:5432/mlflow_db   --default-artifact-root ./mlruns
```

11. MinIO setup
```bash
mkdir -p ${HOME}/minio/data

docker run \
   -p 9000:9000 \
   -p 9001:9001 \
   --user $(id -u):$(id -g) \
   --name minio1 \
   -e "MINIO_ROOT_USER=ROOTUSER" \
   -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
   -v ${HOME}/minio/data:/data \
   quay.io/minio/minio server /data --console-address ":9001"
```
