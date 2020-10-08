import pandas as pd
from src.stock import procStock, corpInfo


def getMyStockInfo():
    df = pd.read_csv("resource/myStockInfo", index_col='index')
    return df

def getMyStockObject(*args):

    if len(args)==0:
        nameArr = ('씨유메디칼', '롯데하이마트', '현대로템', '세틀뱅크', 'PI첨단소재', '동양물산',
                   '수산중공업', '녹십자엠에스', '압타바이오', '이아이디')
    elif len(args)>1:
        raise ValueError('인자가 너무 많습니다.')
    elif type(args[0])!=tuple:
        raise ValueError('리스트, 튜플만 허용 합니다.')
    else:
        nameArr = args[0]

    stockArr = []

    #df = getMyStockInfo()
    corpMap = corpInfo.getMyStockInfoNmCdDict(corpInfo.get_kospi_kosdaq_dataFrame(), nameArr)

    for name in corpMap.keys():
        #stockArr.append(procStock.ProcStock(name, corpMap[name], df))
        stockArr.append(procStock.ProcStock(name, corpMap[name]))
    return stockArr


