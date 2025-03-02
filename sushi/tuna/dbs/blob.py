from google.cloud import storage
from google.cloud.storage import Client
from fastapi import UploadFile
from typing import BinaryIO

storage_client = storage.Client()

class BlobStorage:
    def __init__(self, client: Client, bucket_name: str):
        self.client = client
        self.bucket_name = bucket_name

    def upload_blob(self, file: BinaryIO, path: str):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(path)
        blob.upload_from_file(file, content_type="application/octet-stream")

        file_path = path + "/" + file.name
        b = bucket.blob(file_path)
        return b.generate_signed_url()


