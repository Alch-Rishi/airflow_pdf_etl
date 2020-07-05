from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

pdf_dag = DAG('pdf_service_dag',
            schedule_interval='*/5 * * * *',
            default_args=default_args)

t1 = BashOperator(
    task_id='parse_and_push_to_es',
    bash_command='/usr/local/bin/python /usr/local/airflow/dags/main.py pdf',
    dag=pdf_dag)

t2 = BashOperator(
    task_id='move_error_files',
    bash_command='/usr/local/bin/python /usr/local/airflow/dags/main.py pdf-error',
    dag=pdf_dag)


pdf_dag = DAG('email_service_dag',
            schedule_interval='*/5 * * * *',
            default_args=default_args)

t1 = BashOperator(
    task_id='email_for_ingested_data',
    bash_command='/usr/local/bin/python /usr/local/airflow/dags/main.py pdf',
    dag=pdf_dag)