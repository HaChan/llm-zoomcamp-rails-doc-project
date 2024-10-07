import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from chunking_and_indexing import chunk_and_index_rails_docs

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 29),  # Adjust as needed
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='chunking_and_indexing_docs',
    default_args=default_args,
    schedule_interval=None,
) as dag:
    chunking_and_indexing_task = PythonOperator(
        task_id='chunking_and_indexing_docs',
        python_callable=chunk_and_index_rails_docs,
        provide_context=True,
    )

    chunking_and_indexing_task
