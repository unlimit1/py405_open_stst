import datetime
import pymysql

# CREATE TABLE finance.heartbeat_by_airflow (
#     app_datetime DATETIME(6),
#     db_datetime DATETIME(6),
#     INDEX idx_app_datetime (app_datetime desc)
# );

current_time = datetime.datetime.now()

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

