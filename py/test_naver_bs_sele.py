import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# url = 'https://finance.naver.com/item/coinfo.nhn?code=005930&target=finsum_more'
url = "https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd=005930&amp;target=finsum_more"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


options = Options()
# options.add_argument("--no-sandbox") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
# options.add_argument("--headless") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
# options.add_argument("--disable-dev-shm-usage") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들

driver = webdriver.Chrome(options=options)
driver.get(url)

# 페이지가 로드될 때까지 대기
time.sleep(3)

# old 스타일 : element = driver.find_element_by_id('cns_Tab22') #"분기 탭"
element = driver.find_elements(By.XPATH,'//*[@id="cns_Tab22"]')
print(f'element : [{element}]')
element[0].click()

#HTML을 가져와서 파일로 저장
# page_source = driver.page_source
# file_path = os.path.join('.','py','sele.html')
# print(f'file_path : [{file_path}]')
# with open(file_path, 'w', encoding='utf-8') as f:
#     f.write(page_source)

driver.quit()