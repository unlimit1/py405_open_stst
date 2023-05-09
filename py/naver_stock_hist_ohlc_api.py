import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pymysql
import re
import ast

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
code_list_len = 0

# 네이버 증권의 모든 종목 코드를 가져오는 함수
# 코스피, 코스닥 모두 수집하도록 수정
def get_code():
    # return [['455890','KBSTAR 머니마켓액티브']] # 20230509현재 신규 상장 종목 테스트용 
    code_list = []
    for gu in range (0,2): # 0:코스피, 1:코스닥
        for page in range(1, 100): # 50개씩 나오는 페이지의 크롤링 범위, 코스피는 41 페이지까지지만 충분히 넓게 설정
            res = requests.get(f'https://finance.naver.com/sise/sise_market_sum.nhn?sosok={gu}&page={page}')
            # res.encoding = 'euc-kr'  # 삼천리,ЛяУЕИЎ 로 깨짐.. 인코딩을 수동으로 지정... 해도 개선되지 않음
            soup = BeautifulSoup(res.content, 'lxml') # 파서를 lxml, html.parser 다 적용해보았으나 개선되지 않음
            data = soup.select('div.box_type_l tbody tr')
            for i in data:
                if len(i.select('td')) > 1:
                    code = i.select('a')[0]['href'].split('=')[1]
                    code_name = i.select('a')[0].text
                    code_list.append([code, code_name])
    return code_list

# ohlcv hist 데이터를 가져오는 함수
def get_ohlcv_hist(code):
    # 조회 시작일과 종료일 세팅
    start_date = '19800101' # 충분한 과거 일자

    # 종료일은 현재일자 5일전 일자로 세팅
    end_date = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime('%Y%m%d')

    # API 호출
    # API output 의 가격은 액면분할을 고려한 수정 후 가격이나, 거래량은 수정된 값이 아님... 
    url = f'https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime={start_date}&endTime={end_date}&timeframe=day'
    res = requests.get(url)
    if len(res.content) < 100 : return pd.DataFrame() #신규상장종목으로 데이터가 없으면 헤더문자열만 70byte 만 있으므로 스킵

    # API 호출 결과를 디코딩하여 json으로 변환
    data = res.content.decode('utf-8')
    data = re.sub(r'\s+', '', data)
    data = ast.literal_eval(data)# 문자열 리스트를 파이썬 리스트로 변환
    ohlcv = pd.DataFrame(data[1:], columns=data[0])
    ohlcv.insert(0, '종목코드', code) #df 첫 열에 stock_code 추가
    ohlcv = ohlcv.drop('외국인소진율', axis=1) #df 외국인소진율 열 제거
    return pd.DataFrame(ohlcv)

# 실행 시간 측정
start_time = datetime.datetime.now()

# 모든 종목의 ohlcv 데이터를 가져옴
# all_ohlcv = get_all_ohlcv().reset_index(drop=True)

print(f'종목코드 수집 시작')
code_list = get_code()
code_list_len = len(code_list)
print(f'종목코드 수집 끝 : {code_list_len}')

# DB host 명은 docker-compose.yml 에서 정의한 DB 컨테이너 명
conn = pymysql.connect(host='o_maria', port=int('3666'), user='u_fina', password='dbfinapw', db='finance', charset='utf8')
print(f'DB 접속 성공 : {conn}')
curs = conn.cursor()

print(f'종목별 ohlcv 값 daily hist 수집 및 DB insert 시작')
for i, code in enumerate(code_list):
    print(f'{i}/{code_list_len} code : {code[0]} ', end='')
    ohlcv = get_ohlcv_hist(code[0])

    print(f'크롤링 건수 : {len(ohlcv)} rows')
    ins_values = [tuple(x) for x in ohlcv.values] #df -> tuble list 로 변환
    ins_sql = """
    replace into finance.naver_daily_ohlcv
    (
        stock_code, stock_name, trade_date, open_price, high_price,     low_price, close_price, volume, insert_datetime
    )
    values 
    (   
        %s, '', %s, %s, %s,     %s, %s, %s, now()
    )
    """
    curs.executemany(ins_sql, ins_values)
    conn.commit()
    
print(f'종목별 ohlcv 값 daily hist 수집 및 DB insert 끝')

# 실행 시간 출력
end_time = datetime.datetime.now()
print('Duration: ', end_time - start_time)

curs.close()
conn.close()

print(f'작업 종료')