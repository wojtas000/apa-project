from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")
    database_url: str = os.getenv("DATABASE_URL")
    pool_size: int = os.getenv("POOL_SIZE", 15)
    max_overflow: int = os.getenv("MAX_OVERFLOW", 0)
    embedding_size: int = os.getenv("EMBEDDING_SIZE", 384)
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    rq_timeout: int = os.getenv("RQ_TIMEOUT", 120)
    flair_cache_root: str = os.getenv("FLAIR_CACHE_ROOT")
    entity_similarity_threshold: float = os.getenv("ENTITY_SIMILARITY_THRESHOLD", 0.7)
    app_root: str = str(Path(__file__).resolve().parents[2])

    minio_endpoint: str = os.getenv("MINIO_ENDPOINT")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY")

settings = Settings()
