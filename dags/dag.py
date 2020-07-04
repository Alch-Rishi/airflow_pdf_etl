from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'retry_delay': timedelta(minutes=1),
}

pdf_dag = DAG('pdf_service_dag',
            catchup=False,
            # schedule_interval=timedelta(minutes=2),  # FOR TEST RUN
            schedule_interval="@daily",         # Supports cron expressions for eg. "0/5 * * * *"" for every 5 minute
            default_args=default_args)


email_dag = DAG('email_service_dag',
            catchup=False,
            # schedule_interval=timedelta(minutes=5),   # FOR TEST RUN
            schedule_interval="@weekly",        # Supports cron expressions for eg. "0/5 * * * *"" for every 5 minute
            default_args=default_args)

t1 = BashOperator(
    task_id='parse_and_push_to_es',
    retries=3,
    bash_command='/usr/local/bin/python /usr/local/airflow/main.py pdf',
    dag=pdf_dag)

t2 = BashOperator(
    task_id='move_error_files',
    bash_command='/usr/local/bin/python /usr/local/airflow/main.py pdf-error',
    dag=pdf_dag)


t3 = BashOperator(
    task_id='email_for_ingested_data',
    bash_command='/usr/local/bin/python /usr/local/airflow/main.py email',
    dag=email_dag)


t1 >> t2
