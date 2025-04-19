from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append('/opt/spark/process_raw_to_bronze.py')

from process_raw_to_bronze import process

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='raw_to_bronze_pipeline',
    schedule_interval='@daily',
    default_args=default_args,
    catchup=False,
    tags=["etl"],
) as dag:
    process_data = PythonOperator(
        task_id='process_raw_files',
        python_callable=process,
    )
    process_data