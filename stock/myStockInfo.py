import pandas as pd

def getMyStocInfo():
    df = pd.read_csv("C:/Users/DAL/Documents/GitHub/Pycharm/stock/resource/myStockInfo", index_col='index')
    return df
