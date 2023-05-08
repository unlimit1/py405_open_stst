from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime.utcnow() - timedelta(hours=1),
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=1),
    # 'catchup': True
}

dag = DAG(
    dag_id='airflow_heartbeat',
    default_args=default_args,
    schedule_interval='*/5 * * * *',
    catchup=True,
    max_active_runs=1,
)

bash_task = BashOperator(
    task_id='airflow_heartbeat_bash_ssh',
    bash_command='ssh root@o_ubt python3 /py405_open_stst/py/airflow_heartbeat.py',
    dag=dag
)
