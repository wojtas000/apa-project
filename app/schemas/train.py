from pydantic import BaseModel

class Train(BaseModel):
    dataset_name: str = "dataset"
    from_checkpoint: str | None = "english"
    checkpoint_save_mode: str = "SAVE_FULL_MODEL"
    config: dict = {
        "num_epoch": 1,
        "model": "FAST_LSA_T_V2"
    }

