from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Fix path (directory, not file)
def safe_main_callable():
    from api_request.insert_request import main
    return main()

default_args = {
    'owner': 'ritik',
    'description': "A DAG to orchestrate data",
    'start_date': datetime(2026, 5, 1),
}

dag = DAG(
    dag_id='weather-api-orchestrate',
    default_args=default_args,
    schedule=timedelta(minutes=1),
    catchup=False
)

with dag:
    task1 = PythonOperator(
        task_id='example_task',
        python_callable=safe_main_callable
    )