import boto3

MINIO_ENDPOINT = "http://localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"

BUCKET_NAME = "gastric-cancer"
LOCAL_FILE = "raw/gastric_cancer_detection_dataset.csv"
MINIO_OBJECT = "raw/gastric_cancer_detection_dataset.csv"

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY,
    region_name="us-east-1",
)

s3.upload_file(
    LOCAL_FILE,
    BUCKET_NAME,
    MINIO_OBJECT,
)

print("Dataset uploaded successfully!")

DOWNLOAD_FILE = "downloaded_gastric_cancer_dataset.csv"

s3.download_file(
    BUCKET_NAME,
    MINIO_OBJECT,
    DOWNLOAD_FILE,
)

print("Dataset downloaded successfully!")
