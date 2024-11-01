from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name='api-key', auto_error=False)

def api_key_auth(key: str = Security(api_key_header)):
    if key != settings.api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
