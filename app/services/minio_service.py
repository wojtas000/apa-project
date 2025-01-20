import os
from minio import Minio
from app.core.config import settings


class MinioService:
    def __init__(self):
        self.minio_frontend = settings.minio_frontend
        self.minio_endpoint = settings.minio_endpoint
        self.minio_access_key = settings.minio_access_key
        self.minio_secret_key = settings.minio_secret_key
        self.minio_client = Minio(
            self.minio_endpoint,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=False,
        )

    def get_bucket(self, bucket_name):
        return self.minio_client.bucket_exists(bucket_name)

    def get_object(self, bucket_name, object_name):
        return self.minio_client.get_object(bucket_name, object_name)

    def put_object(self, bucket_name, object_name, data, length):
        return self.minio_client.put_object(
            bucket_name, object_name, data, length
        )

    def remove_object(self, bucket_name, object_name):
        return self.minio_client.remove_object(bucket_name, object_name)

    def list_objects(self, bucket_name):
        return self.minio_client.list_objects(bucket_name)

    def list_buckets(self):
        return self.minio_client.list_buckets()
    
    def download_dataset_from_bucket(self, bucket_name: str, prefix: str, local_dir: str):
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        for obj in self.minio_client.list_objects(bucket_name, prefix=prefix, recursive=True):
            local_file = os.path.join(local_dir, obj.object_name[len(prefix):].lstrip('/'))
            os.makedirs(os.path.dirname(local_file), exist_ok=True)
            self.minio_client.fget_object(bucket_name, obj.object_name, local_file)
