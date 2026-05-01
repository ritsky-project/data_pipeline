from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import os

# =========================
# 🔹 DEFAULT CONFIG
# =========================
default_args = {
    "owner": "ritik",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

# =========================
# 🔹 DAG DEFINITION
# =========================
with DAG(
    dag_id="etl_api_pipeline",
    default_args=default_args,
    description="Simple ETL pipeline from API to local storage",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    # =========================
    # 🔹 TASK 1: EXTRACT
    # =========================
    def extract_data():
        url = "https://jsonplaceholder.typicode.com/posts"
        response = requests.get(url)
        data = response.json()

        with open("/tmp/raw_data.json", "w") as f:
            json.dump(data, f)

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data
    )

    # =========================
    # 🔹 TASK 2: TRANSFORM
    # =========================
    def transform_data():
        with open("/tmp/raw_data.json", "r") as f:
            data = json.load(f)

        # Example: keep only title & id
        transformed = [
            {"id": item["id"], "title": item["title"]}
            for item in data
        ]

        with open("/tmp/transformed_data.json", "w") as f:
            json.dump(transformed, f)

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data
    )

    # =========================
    # 🔹 TASK 3: LOAD
    # =========================
    def load_data():
        with open("/tmp/transformed_data.json", "r") as f:
            data = json.load(f)

        os.makedirs("/tmp/output", exist_ok=True)

        with open("/tmp/output/final_data.json", "w") as f:
            json.dump(data, f)

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data
    )

    # =========================
    # 🔹 PIPELINE FLOW
    # =========================
    extract_task >> transform_task >> load_task