import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_financial_statements(code):
    url = f"https://finance.naver.com/item/main.nhn?code={code}"
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    # 재무제표 테이블을 가져옵니다
    all_fs = bs_obj.find("div", class_="section cop_analysis").find_all("table")

    # 각 재무제표 별로 데이터를 파싱합니다
    financial_statements = []
    for table in all_fs:
        data = []
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) > 0:
                data.append([td.text.strip() for td in tds])
        df = pd.DataFrame(data).set_index(0)
        print(df)
        # df.columns = df.columns.map(str)
        # financial_statements[df.columns[0]] = df.drop(df.columns[0], axis=1).T
    return financial_statements

# 삼성전자의 종목코드는 '005930'
financial_statements = get_financial_statements('005930')
print(financial_statements)

# for key, fs in financial_statements.items():
#     fs.to_csv(f"samsung_{key}.csv", encoding="utf-8-sig")
