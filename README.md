# Quickstart
1. Install packages with
```
pip install -r requirements.txt
```
2. Copy `.env.example` into `.env` and fill the required environmental variables
3. Start fastAPI server by running
```
fastapi run --reload app/main.py
```
alternatively
```
uvicorn app.main:app --reload --reload-dir=app --host=0.0.0.0 --port=8000
```

4. Start redis worker for background task processing with
```
python -m scripts.start_worker

```
5. Background task monitoring at `localhost:8000/rq/`
6. Admin panel at `localhost:8000/admin/`
7. Database backup:
```
docker exec -t <container-id> pg_dump -U postgres postgres > backups/backup.sql

```
8. Database migrations:
```
alembic revision --autogenerate -m "your_migration_message"
alembic upgrade head
```
9. Create requirements.txt (lockfile with all dependencies)
```bash
pip-compile -v --resolver=backtracking requirements.in --output-file requirements.txt
```
10. MLFlow
```bash
mlflow ui   --backend-store-uri postgresql://mlflow_user:mlflow_password@localhost:5432/mlflow_db   --default-artifact-root ./mlruns
```

11. Pyabsa setup:
```bash
!git clone https://github.com/yangheng95/PyABSA --depth=1
%cd PyABSA
!pip install -r requirements.txt
!python setup.py install
```

```python
from pyabsa import download_all_available_datasets

download_all_available_datasets()

from pyabsa import ModelSaveOption, DeviceTypeOption
from pyabsa import AspectPolarityClassification as APC
config = APC.APCConfigManager.get_apc_config_english()
config.num_epoch = 1
config.model = APC.APCModelList.FAST_LSA_T_V2
config.output_dim = 4
config.label_to_index = label_to_index
config.index_to_label = index_to_label
trainer = APC.APCTrainer(
    config=config,
    dataset='200.apa',
    from_checkpoint="english",
    auto_device=DeviceTypeOption.AUTO,
    checkpoint_save_mode=ModelSaveOption.SAVE_FULL_MODEL,
    load_aug=False,
)
```