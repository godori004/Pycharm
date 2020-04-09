import pandas as pd
import pandas_datareader.data as web

gs = web.DataReader("078930.KS", "yahoo", "2014-01-01", "2016-03-06")

print(gs.tail())

ma5 = gs['Adj Close'].rolling(window=5).mean()

type(ma5)

print(ma5.tail(10))

gs['Volume'] != 0

new_gs = gs[gs['Volume'] !=0]

print(new_gs.tail(5))

ma5 = new_gs['Adj Close'].rolling(window=5).mean()

print(ma5.tail(10))