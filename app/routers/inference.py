from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix="/inference", tags=["inference"])