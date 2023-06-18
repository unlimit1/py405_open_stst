import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


#url = 'https://finance.naver.com/item/coinfo.nhn?code=005930&target=finsum_more'
url="https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930&amp;target=finsum_more"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_req1():
    res = requests.get(url)
    # HTML 파일로 저장
    file_path = os.path.join('.','py','comp_crawl','req1.html')
    print(f'file_path : [{file_path}]')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(res.text)

def get_req2():
    res = requests.get(url, headers=headers)
    # HTML 파일로 저장
    file_path = os.path.join('.','py','comp_crawl','req2.html')
    print(f'file_path : [{file_path}]')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(res.text)

def get_selenium():
    options = Options()
    # options.add_argument("--no-sandbox") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
    # options.add_argument("--headless") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
    # options.add_argument("--disable-dev-shm-usage") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # 페이지가 로드될 때까지 5초 대기
    time.sleep(5)

    # HTML을 가져와서 파일로 저장
    page_source = driver.page_source
    file_path = os.path.join('.','py','comp_crawl','sele.html')
    print(f'file_path : [{file_path}]')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page_source)
    driver.quit()

get_req1()
get_req2()
get_selenium()



