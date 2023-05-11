from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime.utcnow() - timedelta(hours=25),
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=1),
    'catchup': True
}

dag = DAG(
    dag_id='naver_stock_daily_ohlc',
    description="네이버증권의 코스피/코스닥 전종목 10일 분 ohlc 데이터 크롤링",
    default_args=default_args,
    schedule_interval='05 18 * * *',
    catchup=True,
    #max_active_runs=1,
)

download_launches = BashOperator(
    task_id="naver_stock_daily_ohlc",
    bash_command="ssh -o StrictHostKeyChecking=no root@o_ubt python3 /py405_open_stst/py/naver_stock_daily_ohlc.py",
    dag=dag,
)