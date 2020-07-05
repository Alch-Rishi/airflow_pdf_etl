from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1)
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('pdf_service_dag',
            schedule_interval='*/5 * * * *',
            default_args=default_args)

t1 = BashOperator(
    task_id='parse_and_push_to_es',
    bash_command='/usr/local/bin/python /usr/local/airflow/dags/test.py',
    dag=dag)