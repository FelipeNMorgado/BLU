import os
from minio import Minio
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return Minio(
        endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        secure=os.getenv("MINIO_SECURE", "false").lower() == "true"
    )

def upload(caminho_local: str, bucket: str, objeto: str):
    client = get_client()
    if not client.bucket_exists(bucket):
        client.make_bucket(bucket)
        print(f"Bucket '{bucket}' criado.")
    client.fput_object(bucket, objeto, caminho_local)
    print(f"✅ {caminho_local} → minio://{bucket}/{objeto}")