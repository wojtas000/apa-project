from fastapi import APIRouter, Depends, HTTPException, status
from app.config import settings
from app.database import get_db
from app.auth import api_key_auth

router = APIRouter(prefix="/etl", tags=["etl"])

@router.get(
    "/", 
    dependencies=[Depends(api_key_auth)],
    response_model_exclude_none=True
)
def get_dummy():
    return {"response": "hello world"}