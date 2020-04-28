from stock import corpInfo
from stock import naverInfo
import pandas as pd

kospi_df  = corpInfo.get_download_kospi()
kosdaq_df = corpInfo.get_download_kosdaq()

name      = "한국공항";
code      = ""; #조회할 코드
url       = ""; #조회할 url

pdData = pd.concat([kospi_df, kosdaq_df])
pdData = pdData[['회사명','종목코드', '업종']]
pdData = pdData.rename(columns={'회사명': 'name', '종목코드': 'code', '업종': 'sector'})
pdData = pdData.fillna('-')

code = corpInfo.get_code(pdData, name)[0:-3]

if code == "Series([]":
    print("코드값 이 없습니다. 에러 발생")
    raise Exception

url = naverInfo.get_url(code)

df = naverInfo.get_price(url);
df = df.dropna()

# 상위 5개 데이터 확인하기
print(df.head())
