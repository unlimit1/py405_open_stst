import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import pymysql

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

url = 'https://finance.naver.com/item/sise_day.nhn?code=005930&page='

# 네이버 증권의 모든 종목 코드를 가져오는 함수
def get_code():
    url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page='
    code_list = []
    for page in range(1, 49): # 50개씩 나오는 페이지의 크롤링 범위, 코스피는 41 페이지까지지만 충분히 넓게 설정
        res = requests.get(url + str(page))
        soup = BeautifulSoup(res.content, 'html.parser')
        data = soup.select('div.box_type_l tbody tr')
        for i in data:
            if len(i.select('td')) > 1:
                code = i.select('a')[0]['href'].split('=')[1]
                code_name = i.select('a')[0].text
                code_list.append([code, code_name])
    return code_list

# ohlcv 데이터를 가져오는 함수
def get_ohlcv(code):
    url = f'https://finance.naver.com/item/sise_day.nhn?code={code[0]}'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.select('table.type2 tr')
    ohlcv = []
    for i in data:
        if len(i.select('td')) == 7:
            date = i.select('td')[0].text.strip().replace('.','-')
            open_price = i.select('td')[3].text.strip().replace(',', '')
            high_price = i.select('td')[4].text.strip().replace(',', '')
            low_price = i.select('td')[5].text.strip().replace(',', '')
            close_price = i.select('td')[1].text.strip().replace(',', '')
            volume = i.select('td')[6].text.strip().replace(',', '')
            ohlcv.append([code[0], code[1].strip(), date, open_price, high_price, low_price, close_price, volume])
    return pd.DataFrame(ohlcv)

# 모든 종목의 ohlcv 데이터를 가져오는 함수
def get_all_ohlcv():
    all_ohlcv = pd.DataFrame()
    print(f'종목코드 수집 시작')
    code_list = get_code()
    print(f'종목코드 수집 끝 : {len(code_list)}')
    print(f'종목별 ohlcv값 수집 시작')
    for i, code in enumerate(code_list):
        ohlcv = get_ohlcv(code)
        ohlcv.columns=['code', 'name', 'date', 'open', 'high', 'low', 'close', 'volume']
        #df = df.set_index('date')
        #df.index = pd.to_datetime(df.index)
        all_ohlcv = pd.concat([all_ohlcv, ohlcv], axis=0)
        
        if i%50 == 0 : print('.', end='', flush=True) 
        if i>0 and i%200 == 0 : print(i, end='', flush=True) 
    print(f'종목별 ohlcv값 수집 끝')
    return all_ohlcv

# 실행 시간 측정
start_time = datetime.datetime.now()

# 모든 종목의 ohlcv 데이터를 가져옴
all_ohlcv = get_all_ohlcv().reset_index(drop=True)

# 실행 시간 출력
end_time = datetime.datetime.now()
print('Duration: ', end_time - start_time)

# DB host 명은 docker-compose.yml 에서 정의한 DB 컨테이너 명
conn = pymysql.connect(host='o_maria', port=int('3666'), user='u_fina', password='fina!@34', db='finance', charset='utf8')
print(f'DB 접속 성공 : {conn}')
curs = conn.cursor()


# all_ohlcv['open'] = all_ohlcv['open'].astype(int) # 요 변환으로도 , 를 처리하지 못함.... 아예 상위 수집단계에서 replace처리
# all_ohlcv df 오류 찾기 위해 파일 생성
# all_ohlcv.to_csv('all_ohlcv-'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.csv') -> 신규 종목은 과거 날짜 데이터가 없어서 오류 발생!
print(f'all_ohlcv 크롤링 건수 : {len(all_ohlcv)} rows')
    # print(all_ohlcv.iloc[200:210])
    # print(all_ohlcv.iloc[200:210,2].apply(lambda x: len(x)))
    # all_ohlcv = all_ohlcv.dropna(subset=['date']) # 이 문장으로 처리가 안되어 아래와 같이 코드 수정
all_ohlcv = all_ohlcv[all_ohlcv['date'] != '']
print(f'all_ohlcv 거래일자 데이터 없는 건 삭제 처리 후 남은 건수 : {len(all_ohlcv)} rows')

ins_values = [tuple(x) for x in all_ohlcv.values] #df -> tuble list 로 변환
ins_sql = """
replace into finance.naver_daily_ohlcv
(
    stock_code, stock_name, trade_date, open_price, high_price,     low_price, close_price, volume, insert_datetime
)
values 
(   
    %s, %s, %s, %s, %s,     %s, %s, %s, now()
)
"""
print(f'DB replace into 시작 : {len(ins_values)} rows')
curs.executemany(ins_sql, ins_values)
conn.commit()
print(f'DB replace into 종료')

curs.close()
conn.close()

print(f'작업 종료')