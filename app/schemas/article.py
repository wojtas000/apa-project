from pydantic import BaseModel

class TrainTestDevSplit(BaseModel):
    dataset_name: str = "dataset"
    with_ambivalent: bool = False
