import os, time, datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pymysql

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# 네이버 증권의 모든 종목 코드를 가져오는 함수
# 코스피, 코스닥 모두 수집하도록 수정
def get_code():
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

# financial_indicator 값을 가져오는 함수
def get_fi(code):
    url = f"https://navercomp.wisereport.co.kr/v2/company/c1010001.aspx?cmp_cd={code[0]}&amp;target=finsum_more"
    print(f"url : {url}")
    options = Options()
    options.add_argument("--no-sandbox") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
    options.add_argument("--headless") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들
    options.add_argument("--disable-dev-shm-usage") #Docker 컨테이너나 리눅스에서 제한된 권한으로 크롬을 실행할 때 필요한 옵션들

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(0.1)     # 페이지가 로드될 때까지 대기

    fi_tab_xpaths = [('//*[@id="cns_Tab21"]','연간'),('//*[@id="cns_Tab22"]','분기')] # 연간, 분기
    
    l_df = [] # 재무지표를 append 하여 임시 보관할 list
    for fi_tab_xpath in fi_tab_xpaths:
        try: # 재무지표 테이블이 없을 때, 해당 element 가 없어서 None 리턴... 클릭시 오류
            element = driver.find_elements(By.XPATH,fi_tab_xpath[0]); 
            element[0].click() # 연간/분기 탭 클릭
        except IndexError:
            print(f"Tab click error : {code}")
            return pd.DataFrame()
        
        page_source = driver.page_source # HTML 가져오기
        tables = pd.read_html(page_source) # pandas read_html 로 html 내 테이블 모두 가져오기
        fi = tables[12] # fi(financial indicator) data_frame
        # read_html 로 크롤링한 df 가공
        fi.columns = fi.columns.droplevel(0) #멀티컬럼에서 불필요 첫 행 컬럼명 부분 ("분기") 제거
        fi.set_index(fi.columns[0],inplace=True) #재무지표명(첫열) 을 인덱스로 반영
        fi.index.rename('주요재무정보', inplace=True) #인덱스 명 수정

        # 테이블 저장을 위해 각 행,렬, 값으로 분해
        cols = list(fi.columns)
        inds = list(fi.index)

        for col in cols:
            for ind in inds:
                # crawling_datetime,stock_code,financial_indicator_name,quarter_ym,year_quarter_cl,accounting_standard_name,prediction_yn,financial_indicator_value,crawling_origin_text
                # crawling_datetime
                stock_code = code[0]
                financial_indicator_name = ind
                quarter_ym = col[0:7].replace('/','')
                year_quarter_cl = fi_tab_xpath[1] # '연간','분기'
                accounting_standard_name = col[-7:-1]
                prediction_yn = 'Y' if col[8] == 'E' else 'N'
                financial_indicator_value = fi.loc[ind, col]  # return 시 read_html 의 nan 처리!
                crawling_origin_text = f"{col}|{ind}|{fi.loc[ind, col]}"
                #print(f"df:[{stock_code},{financial_indicator_name},{quarter_ym},{year_quarter_cl},{accounting_standard_name},{prediction_yn},{financial_indicator_value},{crawling_origin_text}]")
                l_df.append([stock_code, financial_indicator_name,quarter_ym,year_quarter_cl,accounting_standard_name,prediction_yn,financial_indicator_value,crawling_origin_text])
                #print(len(l_df), l_df[-2:])   
    driver.quit()
    # return pd.DataFrame(l_df).fillna(value=Null) # -> raise ValueError("Must specify a fill 'value' or 'method'.")
    return pd.DataFrame(l_df).astype(object).where(pd.notnull(l_df), None) # nan 값 처리!!

# 모든 종목의 financial indicator 데이터를 가져오는 함수
def get_all_fi():
    all_fi = pd.DataFrame()
    print(f'종목코드 수집 시작')
    code_list = get_code()
    print(f'종목코드 수집 끝 : {len(code_list)}')
    print(f'종목별 financial indecator value 수집 시작')
    for i, code in enumerate(code_list):
        fi = get_fi(code)
        if fi.empty: continue # 재무지표 데이터가 없는 경우 skip
        fi.columns=['stock_code', 'financial_indicator_name','quarter_ym','year_quarter_cl','accounting_standard_name','prediction_yn','financial_indicator_value','crawling_origin_text']
        #df = df.set_index('date')
        #df.index = pd.to_datetime(df.index)
        all_fi = pd.concat([all_fi, fi], axis=0)
        # if i%10 == 0 : print('.', end='\n', flush=True) 
        # if i>0 and i%3 == 0 : break  # 테스트용... 적은 범위 수행 위해
        if i>0 and i%10 == 0 : print(f"{i}/{len(code_list)}", end='\n', flush=True) 
    print(f'종목별 financial indecator value 수집 끝')
    return all_fi

# 실행 시간 측정
start_time = datetime.datetime.now()

# 모든 종목의 finanacial indicator 데이터를 가져옴
all_fi = get_all_fi().reset_index(drop=True)

# 실행 시간 출력
end_time = datetime.datetime.now()
print('Duration: ', end_time - start_time)

# # DB host 명은 docker-compose.yml 에서 정의한 DB 컨테이너 명
conn = pymysql.connect(host='o_maria', port=int('3666'), user='u_fina', password='dbfinapw', db='finance', charset='utf8')
print(f'DB 접속 성공 : {conn}')
curs = conn.cursor()


print(f'all_fi 크롤링 건수 : {len(all_fi)} rows')
#     # print(all_ohlcv.iloc[200:210])
#     # print(all_ohlcv.iloc[200:210,2].apply(lambda x: len(x)))
#     # all_ohlcv = all_ohlcv.dropna(subset=['date']) # 이 문장으로 처리가 안되어 아래와 같이 코드 수정
# all_ohlcv = all_ohlcv[all_ohlcv['date'] != '']
# print(f'all_ohlcv 거래일자 데이터 없는 건 삭제 처리 후 남은 건수 : {len(all_ohlcv)} rows')

ins_values = [tuple(x) for x in all_fi.values] #df -> tuble list 로 변환
for i in ins_values: print(i)
ins_sql = """
replace into finance.naver_financial_indicator_value
(
    crawling_datetime, stock_code, financial_indicator_name, quarter_ym, year_quarter_cl
   ,accounting_standard_name, prediction_yn, financial_indicator_value, crawling_origin_text
)
values 
(   
    now(), %s, %s, %s, %s
   ,%s ,%s, %s, %s
)
"""
print(f'DB replace into 시작 : {len(ins_values)} rows')
curs.executemany(ins_sql, ins_values)
conn.commit()
print(f'DB replace into 종료')

curs.close()
conn.close()

print(f'작업 종료')