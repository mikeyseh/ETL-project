"""
Postgres -> S3/MinIO ingestion.

Exports every table from source_db as a CSV and uploads to the `raw-data`
bucket in MinIO. Reproduces the `Airbyte: Postgres -> S3` sync in code.
"""
import os
import io
import boto3
from botocore.client import Config
from sqlalchemy import create_engine, text
import pandas as pd

SOURCE_DB = "postgresql+psycopg2://postgres:secret@source_postgres:5432/source_db"
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
BUCKET = "raw-data"

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

def ensure_bucket(s3):
    try:
        s3.head_bucket(Bucket=BUCKET)
    except Exception:
        s3.create_bucket(Bucket=BUCKET)

def export_table(s3, engine, table):
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    key = f"{table}.csv"
    s3.put_object(Bucket=BUCKET, Key=key, Body=io.BytesIO(csv_bytes), ContentType="text/csv")
    print(f"  Ã¢Å“â€œ {table}  ({len(df)} rows, {len(csv_bytes)} bytes) -> s3://{BUCKET}/{key}")

def main():
    print("Connecting to source DB...")
    engine = create_engine(SOURCE_DB)

    with engine.connect() as conn:
        tables = [r[0] for r in conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename"
        ))]

    print(f"Found {len(tables)} tables: {tables}")
    s3 = get_s3_client()
    ensure_bucket(s3)
    print(f"Uploading to s3://{BUCKET}/ ...")

    for table in tables:
        export_table(s3, engine, table)

    print(f"\nÃ¢Å“â€¦ Ingestion complete: {len(tables)} tables written to MinIO bucket '{BUCKET}'")

if __name__ == "__main__":
    main()