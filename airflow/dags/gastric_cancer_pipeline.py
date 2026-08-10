from airflow.sdk import DAG, task
from datetime import datetime

import boto3

MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

BUCKET_NAME = "gastric-cancer"
MINIO_OBJECT = "raw/gastric_cancer_detection_dataset.csv"

with DAG(
    dag_id="gastric_cancer_pipeline",
    start_date=datetime(2026, 8, 1),
    schedule=None,
    catchup=False,
) as dag:

    @task
    def extract_from_minio():
        s3 = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name="us-east-1",
        )

        local_file = "/tmp/gastric_cancer_detection_dataset.csv"

        s3.download_file(
            BUCKET_NAME,
            MINIO_OBJECT,
            local_file,
        )
        print(f"Dataset downloaded to {local_file}")

        return local_file

    extract_from_minio()
