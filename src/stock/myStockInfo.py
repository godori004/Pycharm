import pandas as pd
from src.stock import procStock, corpInfo


def getMyStockInfo():
    df = pd.read_csv("C:/Users/DAL/Documents/GitHub/Pycharm/src/stock/resource/myStockInfo", index_col='index')
    return df

def getMyStockObject(*args):

    if len(args)==0:
        nameArr = ('엑스큐어', '롯데하이마트', '카스', 'LG디스플레이', '아이진', '윙입푸드', '삼성전자', '네오셈', '한국공항', '비엠티')
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


