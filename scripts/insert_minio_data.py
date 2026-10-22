import os
import logging
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

# Load environment variables
load_dotenv()
minio_access_key = os.getenv('MINIO_ACCESS_KEY')
minio_secret_key = os.getenv('MINIO_SECRET_KEY')
minio_url = os.getenv('MINIO_URL_FOR_INSERTION')
bucket_name = os.getenv('BUCKET_SOURCE_NAME')
object_name = os.getenv('OBJECT_SOURCE_NAME')


logging.basicConfig(level=logging.INFO)


data = {'code': [1, 2, 3], 'name': ['Alice', 'Bob', 'Charlie'], 'salary': [50000.00, 60000.00, 70000.00]}
df = pd.DataFrame(data)

# Convert DataFrame to CSV in an in-memory buffer
csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False, sep=',',encoding='utf-8')
csv_buffer.seek(0)

logging.info("DataFrame converted to CSV in memory.")

# Connect to MinIO client
minio_client = Minio(
    minio_url,
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False
)

try:
    # Check if the bucket exists, create it if it doesn't
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        logging.info(f"Bucket '{bucket_name}' created.")
    else:
        logging.info(f"Bucket '{bucket_name}' already exists.")

    # Upload the CSV file to MinIO
    minio_client.put_object(bucket_name, object_name, csv_buffer, csv_buffer.getbuffer().nbytes)
    logging.info(f"CSV data uploaded to bucket '{bucket_name}' as '{object_name}'.")
except S3Error as e:
    logging.error(f"Error uploading to MinIO: {e}")
