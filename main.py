from datetime import datetime, timedelta


from airflow import DAG
from airflow.operators.python_operator import PythonOperator


from service.pdf_service import process

default_args = {
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 3,
    'retry_delay': timedelta(seconds=5),
    'catchup': False
}

with DAG(   dag_id='core-dag',
            default_args=default_args,
            schedule_interval='*/30 * * * *', ) as dag:
            parse_operator = PythonOperator(
            task_id='parse_files',
            provide_context=True,
            python_callable=process,
            dag=dag,
        )