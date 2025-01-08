from datetime import datetime

import mlflow
import mlflow.pyfunc
from fastapi import APIRouter

from app.core.config import settings
from app.schemas.train import Train

router = APIRouter(prefix="/train", tags=["train"])

@router.post(
    "",
    response_model_exclude_none=True
)
async def train(
    data: Train
):
    from pyabsa import ModelSaveOption, DeviceTypeOption
    from pyabsa import AspectPolarityClassification as APC

    with mlflow.start_run() as run:
        run_name = f"{data.dataset_name}-{data.config.get('model', 'FAST_LSA_T_V2')}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        mlflow.set_tag("mlflow.runName", run_name)

        config = APC.APCConfigManager.get_apc_config_english()
        config.num_epoch = data.config.get("num_epoch", 1)
        config.model = getattr(APC.APCModelList, data.config.get('model', 'FAST_LSA_T_V2'))

        mlflow.log_param("dataset_name", data.dataset_name)
        mlflow.log_param("from_checkpoint", data.from_checkpoint)
        mlflow.log_param("checkpoint_save_mode", data.checkpoint_save_mode)
        mlflow.log_params(config)
        
        save_path = f"{settings.app_root}/ml-models/inference/{run_name}"
        trainer_args = {
            "config": config,
            "dataset": data.dataset_name,
            "auto_device": DeviceTypeOption.AUTO,
            "checkpoint_save_mode": getattr(ModelSaveOption, data.checkpoint_save_mode),
            "load_aug": False,
            "path_to_save": save_path,
        }

        if data.from_checkpoint is not None:
            trainer_args["from_checkpoint"] = data.from_checkpoint

        trainer = APC.APCTrainer(**trainer_args)


        mlflow.log_artifact(save_path, artifact_path=save_path)
