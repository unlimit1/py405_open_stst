from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
import pymysql

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 5, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False
}

dag = DAG(
    'heartbeat_by_airflow',
    default_args=default_args,
    schedule_interval='6,16,26,36,46,56 * * * *',
    executor='LocalExecutor'
)

def insert_current_time():
    current_time = datetime.now()

    conn = pymysql.connect(host='o_maria', port=int('3666'), user='u_fina', password='dbfinapw', db='finance', charset='utf8')
    print(f'DB 접속 성공 : {conn}')
    curs = conn.cursor()

    ins_sql = f"""INSERT INTO heartbeat_by_airflow (app_datetime,    db_datetime) 
        VALUES ('{current_time}',now(6))"""
    print(ins_sql)
    curs.execute(ins_sql)
    conn.commit()
    print(f'DB ins 종료')

    curs.close()
    conn.close()


task = PythonOperator(
    task_id='heartbeat_by_airflow',
    python_callable=insert_current_time,
    dag=dag,
)
