import requests
from bs4 import BeautifulSoup

def get_financial_statements(stock_code):
    url = f'https://finance.naver.com/item/coinfo.nhn?code={stock_code}&target=finsum_more'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    print(url)
    # with open('response.html', 'w') as file:
    #     file.write(response.text)

    # 재무제표 크롤링
    financial_table = soup.find('table', class_='gHead01 all-width')
    print(f'financial_table : {financial_table}')
    financial_data = []
    if financial_table:
        rows = financial_table.find_all('tr')
        print(f'financial_table rows : {rows}')
        for row in rows:
            print(f'row : {row}')
            data = []
            columns = row.find_all('td')
            for column in columns:
                data.append(column.text.strip())
            if data:
                financial_data.append(data)

    # 손익계산서 크롤링
    income_table = soup.find_all('table', class_='gHead01')
    income_data = []
    if len(income_table) > 1:
        rows = income_table[1].find_all('tr')
        for row in rows:
            data = []
            columns = row.find_all('td')
            for column in columns:
                data.append(column.text.strip())
            if data:
                income_data.append(data)

    # 현금흐름표 크롤링
    cashflow_table = soup.find_all('table', class_='gHead01')
    cashflow_data = []
    if len(cashflow_table) > 2:
        rows = cashflow_table[2].find_all('tr')
        for row in rows:
            data = []
            columns = row.find_all('td')
            for column in columns:
                data.append(column.text.strip())
            if data:
                cashflow_data.append(data)

    return {
        'financial_statements': financial_data,
        'income_statement': income_data,
        'cashflow_statement': cashflow_data
    }

# 종목 코드 입력
stock_code = '005930'  # 삼성전자 종목 코드

# 재무제표, 손익계산서, 현금흐름표 크롤링
result = get_financial_statements(stock_code)

# 크롤링 결과 출력
print('재무제표:')
for row in result['financial_statements']:
    print(row)

print('손익계산서:')
for row in result['income_statement']:
    print(row)

print('현금흐름표:')
for row in result['cashflow_statement']:
    print(row)
