import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the url to crawl
url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page='

# Define the number of pages to crawl
pages = 10

# Define empty list to store data
data = []

i=0
for page_num in range(1, pages+1):
    print(f"{i} ", end='')
    # 현재 페이지의 HTML 코드 가져오기
    response = requests.get(url+str(page_num))
    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.content, 'html.parser')
    # HTML 코드에서 두 번째 테이블 태그 가져오기
    table = soup.find_all('table')[1]
    # pandas의 read_html 함수를 사용하여 테이블 태그를 데이터프레임으로 변환
    df = pd.read_html(str(table))[0]
    df.dropna()
    # 필요한 열만 선택
    #df = df[['종목명', '현재가', '전일비', '등락률', '시가', '고가', '저가', '거래량']]
    #df = df[['N', '종목명', '현재가', '전일비', '등락률', '액면가', '시가총액', '상장주식수', '외국인비율', '거래량', 'PER', 'ROE', '토론실']]
    # 열 이름 변경
    # df.columns = ['Name', 'Price', 'Diff', 'Change', 'Open', 'High', 'Low', 'Volume']
    # 데이터프레임을 리스트에 추가
    data.append(df)
    # 1초 대기
    #time.sleep(0.1)

# Concatenate all data into one dataframe
result = pd.concat(data)

# Save the result as csv file
result.to_csv('naver_stock.csv', index=False)

