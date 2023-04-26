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

for page_num in range(1, pages+1):
    print(f"{page_num} ", end='')
    response = requests.get(url+str(page_num))
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find_all('table')[1]
    df = pd.read_html(str(table), encoding='utf-8')[0]
    # 결측값이 있는 행 제거
    df = df.dropna(how='all')
    # 'N' 열의 데이터 타입을 정수형으로 변환
    df['N'] = df['N'].astype(int)
    # 변환된 데이터프레임을 리스트에 추가
    data.append(df)

# Concatenate all data into one dataframe
result = pd.concat(data)

# Save the result as csv file
file_name = 'naver_stock.csv'
result.to_csv(file_name, index=False)

with open(file_name, 'r') as f: data = f.read()
with open(file_name, 'w') as f: f.write('현재 시각 : ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n' + data)
