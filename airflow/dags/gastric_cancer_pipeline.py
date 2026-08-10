from datetime import datetime
from unittest import result

import boto3
from airflow.sdk import DAG, task  # type: ignore

from src.preprocessing.preprocess import preprocess_data

from src.training.train import train_model

from src.evaluation.evaluate import evaluate_model

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

    @task
    def preprocess_dataset(input_path):
        output_path = "/tmp/cleaned_gastric_cancer_dataset.csv"
        result = preprocess_data(input_path, output_path)
        print(f"Preprocessed dataset saved to {result}")
        return result

    @task
    def train_dataset(input_path):
        model_output_path = "/tmp/gastric_cancer_model.pkl"

        train_model(
            input_path,
            model_output_path,
        )

        print("Model training completed successfully.")

        return model_output_path

    @task
    def evaluate_dataset(input_path, model_path):
        metrics_output_path = "/tmp/gastric_cancer_metrics.json"

        evaluate_model(
            input_path,
            model_path,
            metrics_output_path,
        )

        print("Model evaluation completed successfully.")
        print(f"Metrics saved to: {metrics_output_path}")

        print("Model evaluation completed successfully.")
        print(f"Metrics saved to: {metrics_output_path}")
        return metrics_output_path

    raw_data = extract_from_minio()
    cleaned_data = preprocess_dataset(raw_data)
    trained_model = train_dataset(cleaned_data)
    evaluation_metrics = evaluate_dataset(
        cleaned_data,
        trained_model,
    )
