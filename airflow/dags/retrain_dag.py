from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='retrain_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=["ml", "retrain"]
) as dag:

    run_raw_to_bronze = BashOperator(
        task_id='run_raw_to_bronze',
        bash_command='docker exec spark_app /opt/bitnami/spark/bin/spark-submit /opt/spark/process_raw_to_bronze.py'

    )

    run_bronze_to_silver = BashOperator(
        task_id='run_bronze_to_silver',
        bash_command='docker exec spark_app /opt/bitnami/spark/bin/spark-submit /opt/spark/process_bronze_to_silver.py'

    )

    run_raw_to_bronze >> run_bronze_to_silver