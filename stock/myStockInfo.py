import pandas as pd
from stock import corpInfo, procStock

def getMyStockInfo():
    df = pd.read_csv("C:/Users/DAL/Documents/GitHub/Pycharm/stock/resource/myStockInfo", index_col='index')
    return df

def getMyStockObject(*args):

    if len(args)==0:
        nameArr = ('엑스큐어', '세틀뱅크', '롯데하이마트', '카스', 'LG디스플레이', '아이진', '다우기술', '윙입푸드', '에스폴리텍', '에이치엘비파워', '네오셈', '아시아나IDT')
    elif len(args)>1:
        raise ValueError('인자가 너무 많습니다.')
    elif type(args[0])!=tuple:
        raise ValueError('리스트, 튜플만 허용 합니다.')
    else:
        nameArr = args[0]

    stockArr = []

    df = getMyStockInfo()
    corpMap = corpInfo.getMyStockInfoNmCdDict(corpInfo.get_kospi_kosdaq_dataFrame(), nameArr)

    for name in corpMap.keys():
        stockArr.append(procStock.ProcStock(name, corpMap[name], df))

    return stockArr


