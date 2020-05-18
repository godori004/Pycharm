from stock import *
import pandas as pd
import time

kospi_df  = corpInfo.get_download_kospi()
kosdaq_df = corpInfo.get_download_kosdaq()

nameArr = ['한국공항','엑스큐어','세틀뱅크','롯데하이마트','에이치엘비파워','윙입푸드','성우하이텍','카스','LG디스플레이','주연테크', '아이진', '아시아나IDT', '에스폴리텍']
codeArr = []
corpMap = {}

pdData = pd.concat([kospi_df, kosdaq_df])
pdData = pdData[['회사명','종목코드', '업종']]
pdData = pdData.rename(columns={'회사명': 'name', '종목코드': 'code', '업종': 'sector'})
pdData = pdData.fillna('-')

for name in nameArr:
    corpMap[name] = corpInfo.get_code(pdData, name)[0:-3]

while True:
    for key in corpMap.keys():
        test = procStock.ProcStock(corpMap[key])
        print("{} : {}".format(key, test.getCurrentValueStr()))
    print('-----------------------------------------------------')
    time.sleep(20)



#code = corpInfo.get_code(pdData, name)[0:-3]

#test = procStock.ProcStock(code)
#print(test.getCurrentVale())

#url = naverInfo.get_url(code)
#df = naverInfo.get_price(url);
#df = df.dropna()
# 상위 1개 데이터 확인하기
#df = df.head(1);

#value = df.get('종가')[1]

#print(value)

#if value > 48000:
 #   print("now")
#df.to_csv("test.txt", encoding="euc-kr")
