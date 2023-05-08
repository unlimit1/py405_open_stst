from datetime import datetime, timedelta
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG(
    dag_id="naver_stock_daily_ohlc",
    description="photo backup : synology photo -> lim_photo -> google pixel",
    #start_date=datetime(2023,3,23),
    start_date=airflow.utils.dates.days_ago(0.125),
    schedule_interval="05 18 * * *",
    #catchup=False, #재 기동시 start_date 부터 백필?되는 것을 막아준다고 함.
)

download_launches = BashOperator(
    task_id="naver_stock_daily_ohlc",
    bash_command="ssh root@o_ubt python3 /py405_open_stst/py/naver_stock_daily_ohlc.py",
    dag=dag,
)