import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

url = 'https://finance.naver.com/item/sise_day.nhn?code=005930&page='

# 네이버 증권의 모든 종목 코드를 가져오는 함수
def get_code():
    url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page='
    code_list = []
    for page in range(1, 2): # 50개씩 나오는 페이지의 크롤링 범위
        res = requests.get(url + str(page))
        soup = BeautifulSoup(res.content, 'html.parser')
        data = soup.select('div.box_type_l tbody tr')
        for i in data:
            if len(i.select('td')) > 1:
                code = i.select('a')[0]['href'].split('=')[1]
                code_list.append(code)
    return code_list

# ohlcv 데이터를 가져오는 함수
def get_ohlcv(code):
    url = f'https://finance.naver.com/item/sise_day.nhn?code={code}'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    data = soup.select('table.type2 tr')
    ohlcv = []
    for i in data:
        if len(i.select('td')) == 7:
            date = i.select('td')[0].text.strip().replace('.','-')
            open_price = i.select('td')[3].text.strip()
            high_price = i.select('td')[4].text.strip()
            low_price = i.select('td')[5].text.strip()
            close_price = i.select('td')[1].text.strip()
            volume = i.select('td')[6].text.strip()
            ohlcv.append([code, date, open_price, high_price, low_price, close_price, volume])
    return ohlcv

# 모든 종목의 ohlcv 데이터를 가져오는 함수
def get_all_ohlcv():
    code_list = get_code()
    all_ohlcv = []
    for code in code_list:
        print(f'stock_code:{code}')
        ohlcv = get_ohlcv(code)
        print(ohlcv)
        #df = pd.DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        #df = df.set_index('date')
        #df.index = pd.to_datetime(df.index)
        all_ohlcv = all_ohlcv.append(ohlcv)
        print(all_ohlcv)
    return all_ohlcv

# 실행 시간 측정
start_time = datetime.datetime.now()

# 모든 종목의 ohlcv 데이터를 가져옴
all_ohlcv = get_all_ohlcv()
print(all_ohlcv.iloc[0:100,:])


# 실행 시간 출력
end_time = datetime.datetime.now()
print('Duration: ', end_time - start_time)