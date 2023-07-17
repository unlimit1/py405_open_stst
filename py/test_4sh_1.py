import requests
import json

# OpenDART API 키 설정
api_key = '1b0538e85536d493c69b841697d9338375619412'

# 삼성전자의 고유 번호
corp_code = '00126380'

# 특정 분기 설정 
# 1분기보고서 : 11013
# 반기보고서 : 11012
# 3분기보고서 : 11014
# 사업보고서 : 11011
year = 2023
quarter = '11013' 


# OpenDART API URL 생성
url = f'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={api_key}&corp_code={corp_code}&bsns_year={year}&reprt_code={quarter}&fs_div=OFS'

# API 요청
response = requests.get(url)

# 응답을 JSON으로 변환
data = response.json()
# for item in data['list']: print(f"[{item['account_id']} {item['account_nm']}] : {item['thstrm_amount']}")

# 필요한 데이터 추출
sales = None
current_assets = None
total_assets = None
total_liabilities = None
total_equity = None
net_income = None

for item in data['list']:
    if item['sj_div'] == 'BS' and item['account_nm'] == '유동자산':
        current_assets = item['thstrm_amount']
    elif item['sj_div'] == 'BS' and item['account_nm'] == '자산총계':
        total_assets = item['thstrm_amount']
    elif item['sj_div'] == 'BS' and item['account_nm'] == '부채총계':
        total_liabilities = item['thstrm_amount']
    elif item['sj_div'] == 'BS' and item['account_nm'] == '자본총계':
        total_equity = item['thstrm_amount']
    elif item['sj_div'] == 'IS' and item['account_nm'] == '수익(매출액)':
        sales = item['thstrm_amount']
    elif item['sj_div'] == 'IS' and item['account_nm'] == '매출총이익':
        income1 = item['thstrm_amount']
    elif item['sj_div'] == 'IS' and item['account_nm'] == '영업이익':
        income2 = item['thstrm_amount']
    elif item['sj_div'] == 'IS' and item['account_nm'] == '금융수익':
        income3 = item['thstrm_amount']
    elif item['sj_div'] == 'IS' and item['account_nm'] == '당기순이익(손실)':
        income4 = item['thstrm_amount']

# 결과 출력
print(f'-- 특정 항목 결과 출력 ----- dart기업코드:{corp_code}  년도-분기:{year}-{quarter}')
print('수익(매출액):    ', format(int(sales), ',').rjust(20))
print('유동자산:        ', format(int(current_assets), ',').rjust(20))
print('자산총계:        ', format(int(total_assets), ',').rjust(20))
print('부채총계:        ', format(int(total_liabilities), ',').rjust(20))
print('자본총계:        ', format(int(total_equity), ',').rjust(20))
print('매출총이익:      ', format(int(income1), ',').rjust(20))
print('영업이익:        ', format(int(income2), ',').rjust(20))
print('금융수익:        ', format(int(income3), ',').rjust(20))
print('당기순이익(손실):', format(int(income4), ',').rjust(20))
