from stock import *
import pandas as pd
import time

#kospi_df  = corpInfo.get_download_kospi()
#kosdaq_df = corpInfo.get_download_kosdaq()
mysInfo_df = myStockInfo.getMyStocInfo()

nameArr = ('엑스큐어','세틀뱅크','롯데하이마트', '카스','LG디스플레이','아이진', '아시아나IDT', '윙입푸드', '에스폴리텍', '에이치엘비파워','네오셈', '원익IPS')
codeArr = []
corpMap = {}

pdData = corpInfo.get_concat_corpInfo(corpInfo.get_download_kospi(), corpInfo.get_download_kosdaq())

for name in nameArr:
    corpMap[name] = corpInfo.get_code(pdData, name)[0:-3]

while True:
    for key in corpMap.keys():
        test = procStock.ProcStock(corpMap[key])
        tmp = "{} : {}|".format(key, test.getCurrentValueStr())
        print(tmp, end='')

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
