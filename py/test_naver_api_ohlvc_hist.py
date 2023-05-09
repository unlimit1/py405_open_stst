import requests, re, ast
import pandas as pd

# 조회할 종목 코드
code = '000660' # 455890 UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb3 in position 4: invalid start byte
                #신규상장 종목은 해당 일자 범위의 데이터가 아예 없다!!
# 조회 시작일과 종료일
start_date = '19800101'; end_date = '20230504'

# API 호출
# API output 의 가격은 액면분할을 고려한 수정 후 가격이나, 거래량은 수정된 값이 아님... 
url = f'https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime={start_date}&endTime={end_date}&timeframe=day'
print(url) 
res = requests.get(url)

# API 호출 결과를 디코딩하여 json으로 변환
print(f'len(res.content) : {len(res.content)}')
data = res.content.decode('utf-8')
data = re.sub(r'\s+', '', data)
data = ast.literal_eval(data)# 문자열 리스트를 파이썬 리스트로 변환
df = pd.DataFrame(data[1:], columns=data[0])
df.insert(0, 'code', code) #df 첫 열에 stock_code 추가
print(df)

#  코스피와 코스닥 종목코드 및 종목명 한국 증권 거래소 크롤링  