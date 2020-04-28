from pandas import Series, DataFrame

mystock = ['kakao', 'naver']

print(mystock[0])
print(mystock[1])

print('--------------------------')

for stock in mystock:
    print(stock)

print('--------------------------')

exam_dic = {
            'key1': 'room1'
            , 'key2': 'room2'
            }

print(exam_dic['key1'])
print(exam_dic['key2'])

print('?--------------------------')

kakao = Series([92600, 92400, 92100, 94300, 92300], index=['2016-02-19', '2016-02-18', '2016-02-17', '2016-02-16', '2016-02-15'])
print(kakao)

print('--------------------------')



kakao_daily_ending_prices  = {'2016-02-19':'92600', '2016-02-18':'92400', '2016-02-17':'92100', '2016-02-16':'94300', '2016-02-15':'92300'}

for date in kakao_daily_ending_prices :
    print("%s : %s" % (date, kakao_daily_ending_prices[date]))



daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

daeshin_day = DataFrame(daeshin)
print(daeshin_day)

print('--------------------------')

raw_data = {'col0':[1,2,3,4],
            'col1':[10,20,30,40],
            'col2':[100,200,300,400]
            }

data = DataFrame(raw_data)
print(data)
print('--------------------------')

daeshin = {'open':  [11650, 11100, 11200, 11100, 11000],
           'high':  [12100, 11800, 11200, 11100, 11150],
           'low' :  [11600, 11050, 10900, 10950, 10900],
           'close': [11900, 11600, 11000, 11100, 11050]}

daeshin_day = DataFrame(daeshin)
print(daeshin_day)

date = ['16.02.29', '16.02.26', '16.02.25', '16.02.24', '16.02.23']
daeshin_day = DataFrame(daeshin, columns=['open', 'high', 'low', 'close'], index=date)
print(daeshin_day)

close = daeshin_day['close']
print(close)

print(daeshin_day['16.02.24'])

day_data = daeshin_day.loc['16.02.24']
print(day_data)
print(type(day_data))


print('--------------------------')