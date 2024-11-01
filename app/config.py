from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")
    database_url: str = os.getenv("DATABASE_URL")
    pool_size: int = os.getenv("POOL_SIZE", 15)
    max_overflow: int = os.getenv("MAX_OVERFLOW", 0)

settings = Settings()