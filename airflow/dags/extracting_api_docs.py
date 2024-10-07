import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from rails_api_scraper_parallel import parallel_scrape_rails_api

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 29),  # Adjust as needed
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='extract_api_docs',
    default_args=default_args,
    schedule_interval=None,
) as dag:
    extract_api_docs_task = PythonOperator(
        task_id='extract_docs',
        python_callable=parallel_scrape_rails_api,
        provide_context=True,
    )

    extract_api_docs_task
