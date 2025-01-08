from fastapi import APIRouter
from pathlib import Path

from app.core.config import settings

router = APIRouter(prefix="/dataset", tags=["dataset"])

@router.get(
    "",
    response_model_exclude_none=True
)
async def get_datasets():
    root_path = Path(settings.app_root)
    dataset_path = root_path / "integrated_datasets/apc"
    return {
        "datasets": sorted([d.name for d in dataset_path.iterdir() if d.is_dir()])
    }