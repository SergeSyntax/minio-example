# get object meta information https://docs.min.io/minio/baremetal/sdk/python
from minio import Minio
from minio.commonconfig import CopySource
from minio.deleteobjects import DeleteObject
import os

# print('test')
endpoint = os.getenv("MIO_ENDPOINT", "localhost:9000")
access_key = os.getenv("MIO_ACCESS_KEY", "minioadmin")
secret_key = os.getenv("MIO_SECRET_KEY", "minioadmin")
# # disable tls in dev
secure = os.getenv("MIO_SECURE", "false").strip().lower() == "true"
bucket_name = os.getenv("MIO_BUCKET_NAME", "dev")
client = Minio(endpoint, access_key, secret_key, secure=secure)

buckets = client.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)

bucket_name = buckets.pop().name
file_path = "./config/loki.yaml"
object_name = "loki.yaml"

#  upload files


client.fput_object(bucket_name, object_name, file_path)

try:
    response = client.get_object(bucket_name, object_name)
    print(response.geturl())
except Exception as err:
    print("failed get an object", err)


meta = client.stat_object(bucket_name, object_name)
print(meta.content_type)
print(meta.last_modified)


result = client.copy_object(
    bucket_name, "prefix/test.yaml", CopySource(bucket_name, object_name)
)

print(result.object_name)

for i in range(10):
    result = client.copy_object(
        bucket_name, f"raw/opensky-{str(i)}.yaml", CopySource(bucket_name, object_name)
    )
    print(result.object_name)


client.remove_object(bucket_name, object_name)


for object in client.list_objects(bucket_name):
    print(object.bucket_name)


delete_object_list = map(
    lambda x: DeleteObject(x.object_name),
    client.list_objects(bucket_name, "prefix/", recursive=True),
)
errors = client.remove_objects(bucket_name, delete_object_list)
for error in errors:
    print("Error while deleting object: ", error)
