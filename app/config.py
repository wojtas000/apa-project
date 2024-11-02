from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")
    database_url: str = os.getenv("DATABASE_URL")
    pool_size: int = os.getenv("POOL_SIZE", 15)
    max_overflow: int = os.getenv("MAX_OVERFLOW", 0)
    embedding_size: int = os.getenv("EMBEDDING_SIZE", 384)
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

settings = Settings()