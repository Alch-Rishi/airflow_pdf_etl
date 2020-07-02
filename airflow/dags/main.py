from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
taskId="complete"+str(datetime(2018,1,1))
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('milestone_one',
            schedule_interval='*/5 * * * *',
            default_args=default_args)

t1 = BashOperator(
    task_id='Complete9_etlpart1',
    bash_command='/usr/local/bin/python /usr/local/etl/test.py',
    dag=dag)
