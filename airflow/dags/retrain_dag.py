from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG('raw_to_bronze_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    run_spark_job = BashOperator(
        task_id='run_spark_preprocessing',
        bash_command='docker exec spark_app spark-submit /opt/process_raw_to_bronze.py'
    )