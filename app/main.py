from minio import Minio
import os

endpoint = os.getenv("MIO_ENDPOINT", "localhost:9000")
access_key = os.getenv("MIO_ACCESS_KEY", "devuser")
secret_key = os.getenv("MIO_SECRET_KEY", "devpassword")
# disable tls in dev
secure = os.getenv("MIO_SECURE", "false").strip().lower() == "true"
bucket_name = os.getenv("MIO_BUCKET_NAME", "dev")
client = Minio(endpoint, access_key, secret_key, secure=secure)

buckets = client.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)
