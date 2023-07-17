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
    dag_id='naver_stock_financial_indicator_value_hist',
    description="네이버 증권의 기업 재무지표 연간/분기 별 데이터 크롤링",
    default_args=default_args,
    schedule_interval='0 19 * * *', # 0분 3시   매주일요일 -> 매일
    catchup=True,
    #max_active_runs=1,
)

download_launches = BashOperator(
    task_id="naver_stock_financial_indicator_value_hist",
    bash_command="ssh -o StrictHostKeyChecking=no root@o_ubt python3 -u /py405_open_stst/py/naver_stock_financial_indicator_value_hist.py",
    dag=dag,
)