# URL = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020202'
r = requests.get(URL)

for i,df in enumerate(pd.read_html(r.text)):
  print(f"[{i}]------------------------------------------- \n{df}")

# df = pd.read_html(r.text)[8]
# df.set_index(df.columns[0],inplace=True)
# df.index.rename('주요재무정보', inplace=True)
# df.columns = df.columns.droplevel(2)
# print(df)
# annual_date = pd.DataFrame(df).xs('최근 연간 실적',axis=1)
# quater_date = pd.DataFrame(df).xs('최근 분기 실적',axis=1)