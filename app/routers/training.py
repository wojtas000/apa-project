from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/training", tags=["training"])