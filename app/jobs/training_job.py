import os
import shutil
from datetime import datetime

from redis.utils import from_url
from rq import Queue, Retry
import mlflow
import mlflow.pyfunc

from app.core.config import settings
from app.schemas.train import Train
from app.services import MinioService

queue = Queue('training', connection=from_url(settings.redis_url), default_timeout=settings.rq_timeout)
minio_service = MinioService()

def enqueue_training(dataset_name: str, config: dict, from_checkpoint: str = "english", checkpoint_save_mode: str = "SAVE_FULL_MODEL"):
    return queue.enqueue_call(
        func=train_model,
        args=(dataset_name, config, from_checkpoint, checkpoint_save_mode),
        result_ttl=2000,
        retry=Retry(max=1)
    )

async def train_model(dataset_name: str, config: dict, from_checkpoint: str = "english", checkpoint_save_mode: str = "SAVE_FULL_MODEL"):
    from pyabsa import ModelSaveOption, DeviceTypeOption
    from pyabsa import AspectPolarityClassification as APC

    temp_folder = f"{settings.app_root}/integrated_datasets/apc/{dataset_name}"

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    minio_service.download_dataset_from_bucket(bucket_name="datasets", prefix=dataset_name, local_dir=temp_folder)

    with mlflow.start_run() as run:
        run_name = f"{dataset_name}-{config.get('model', 'FAST_LSA_T_V2')}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        mlflow.set_tag("mlflow.runName", run_name)

        cfg = APC.APCConfigManager.get_apc_config_english()
        cfg.num_epoch = config.get("num_epoch", 1)
        cfg.model = getattr(APC.APCModelList, config.get('model', 'FAST_LSA_T_V2'))

        mlflow.log_param("dataset_name", dataset_name)
        mlflow.log_param("from_checkpoint", from_checkpoint)
        mlflow.log_param("checkpoint_save_mode", checkpoint_save_mode)
        mlflow.log_params(cfg)
        
        save_path = f"{settings.app_root}/ml-models/inference/{run_name}"
        trainer_args = {
            "config": cfg,
            "dataset": dataset_name,
            "auto_device": DeviceTypeOption.AUTO,
            "checkpoint_save_mode": getattr(ModelSaveOption, checkpoint_save_mode),
            "load_aug": False,
            "path_to_save": save_path,
        }

        if from_checkpoint is not None:
            trainer_args["from_checkpoint"] = from_checkpoint

        trainer = APC.APCTrainer(**trainer_args)

        mlflow.log_artifact(save_path, artifact_path=save_path)

    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)

    return run.info.run_id