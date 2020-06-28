from datetime import datetime, timedelta


from airflow import DAG
from airflow.operators.python_operator import PythonOperator


from processor.pdf_processor import process

mail_to = ['test.test@domain.io'] # will be used for weekly emails

default_args = {
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': mail_to,
    'email_on_success': False,
    'email_on_failure': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=5),
    'catchup': False
}

with DAG(dag_id='core-dag',
             default_args=default_args,
             schedule_interval='*/30 * * * *', ) as dag:
    parse_operator = PythonOperator(
        task_id='parse_files',
        provide_context=True,
        python_callable=process,
        dag=dag,
    )