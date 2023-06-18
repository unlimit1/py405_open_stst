import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

import pandas as pd

url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930&amp;target=finsum_more"
options = Options()
options.add_argument("--no-sandbox") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
options.add_argument("--headless") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
options.add_argument("--disable-dev-shm-usage") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들

driver = webdriver.Chrome(options=options)
driver.get(url)

# 페이지가 로드될 때까지 대기
time.sleep(1)

# 분기 탭 클릭
element = driver.find_elements(By.XPATH,'//*[@id="cns_Tab22"]')
element[0].click()

# 투자의견 컨센서스 펼치기
element = driver.find_elements(By.CLASS_NAME ,'btn_more')
element[0].click()

# HTML 가져오기
page_source = driver.page_source

# pandas read_html 로 html 내 테이블 모두 가져오기
tables = pd.read_html(page_source)

# for i,df in enumerate(tables):
#   print(f"[{i}]------------------------------------------- \n{df}")

# FS(financial summary) df
fs = tables[12]
print(f'fs : -----------------------------\n{fs}')
print(f'fs.columns : -----------------------------\n{fs.columns}')
print(f'fs.index : -----------------------------\n{fs.index}')
print(f'fs.columns[0] : -----------------------------\n{fs.columns[0]}')
print(f'fs.columns[1] : -----------------------------\n{fs.columns[1]}')
print(f'fs.columns[1][1] : -----------------------------\n{fs.columns[1][1]}')
print(f'fs.columns.droplevel(0) : -----------------------------\n{fs.columns.droplevel(0)}')

# df 가공 [ 출처: https://seong6496.tistory.com/156 ]
#   1) 멀티 인덱스 컬럼 첫줄 [0] 삭제 : fs.columns.droplevel(0)
#   2) 첫번째 컬럼을 인덱스로 : df.set_index(df.columns[0],inplace=True)

fs.columns = fs.columns.droplevel(0)
fs.set_index(fs.columns[0],inplace=True)
fs.index.rename('주요재무정보', inplace=True)
print(f'fs : 가공 후---------------------------\n{fs}')

# 테이블 저장을 위해 각 행,렬, 값으로 분해
cols = list(fs.columns)
inds = list(fs.index)

i = 0
for col in cols:
    for ind in inds:
        i += 1
        print(str(i).zfill(4), col, ind, fs.loc[ind, col])

driver.quit()