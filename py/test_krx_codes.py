import requests
from bs4 import BeautifulSoup
import pandas as pd

# 코스피 종목코드 크롤링
kospi_url = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
kospi_data = requests.get(kospi_url).content
kospi_df = pd.read_html(kospi_data, header=0)[0]
kospi_df = kospi_df[['종목코드', '회사명']]
kospi_df = kospi_df.rename(columns={'종목코드': 'code', '회사명': 'company'})
kospi_df.code = kospi_df.code.map('{:06d}'.format)
kospi_df = kospi_df.sort_values(by='code')
kospi_df = kospi_df.reset_index(drop=True)

print (kospi_df)


# 코스닥 종목코드 크롤링  ....  데이터 건수가 160여건 밖에 안되어 활용도가 약함... 왜 160건 밖에?
kosdaq_url = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=16"
kosdaq_data = requests.get(kosdaq_url).content
kosdaq_df = pd.read_html(kosdaq_data, header=0)[0]
kosdaq_df = kosdaq_df[['종목코드', '회사명']]
kosdaq_df = kosdaq_df.rename(columns={'종목코드': 'code', '회사명': 'company'})
kosdaq_df.code = kosdaq_df.code.map('{:06d}'.format)
kosdaq_df = kosdaq_df.sort_values(by='code')
kosdaq_df = kosdaq_df.reset_index(drop=True)


print (kosdaq_df)

