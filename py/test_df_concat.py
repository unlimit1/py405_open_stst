import pandas as pd
import numpy as np

# 첫번째 데이터프레임 생성
df1 = pd.DataFrame(np.random.rand(5, 3))

# 두번째 데이터프레임 생성
df2 = pd.DataFrame(np.random.rand(5, 3))

print(df1)
print(df2)

# 두 데이터프레임을 가로 방향으로 합치기
result = pd.concat([df1, df2], axis=0)

print(df1)
print('---')
print(df2)
print('---')
print(result)