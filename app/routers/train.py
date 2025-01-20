from fastapi import APIRouter

from app.schemas.train import Train
from app.jobs.training_job import enqueue_training

router = APIRouter(prefix="/train", tags=["train"])

@router.post(
    "",
    response_model_exclude_none=True
)
async def train(
    data: Train
):
    enqueue_training(
        dataset_name=data.dataset_name,
        config=data.config,
        from_checkpoint=data.from_checkpoint,
        checkpoint_save_mode=data.checkpoint_save_mode
    )
    return {"message": "Training job enqueued."}
