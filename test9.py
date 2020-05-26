import pandas as pd

df = pd.read_csv("C:/Users/DAL/Documents/GitHub/Pycharm/stock/resource/myStockInfo", index_col='index')

print(df)

print(df.query("index=='{}'".format('윙입푸드')['code']))


