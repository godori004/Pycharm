import urllib3
import json
import pandas


serviceKey = 'aU4owX9qs6yzEJFLxCKhCXcPJOIjXy%2BjXdIawwYd2CrJlYY%2BXQWWDqVflc09iGIcqy88ZNKyl4z%2F1d2%2B%2FOvDtw%3D%3D'
serviceKey = 'aU4owX9qs6yzEJFLxCKhCXcPJOIjXy+jXdIawwYd2CrJlYY+XQWWDqVflc09iGIcqy88ZNKyl4z/1d2+/OvDtw=='

url = 'http://apis.data.go.kr/1360000/LivingWthrIdxService/getHeatFeelingIdx'
url = ''
#url = '127.0.0.1:5000/user'
#url = 'http://apis.data.go.kr/1360000/LivingWthrIdxService/'

url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'

rf = open("C:/Temp/weather_ASOS_areaCode.csv", 'r')
wf = open("C:/Temp/result.csv", 'a')

i=0
arr=[]

while True:
    line = rf.readline()
    i = i+1
    if not line: break
    #파일의 첫번째 라인 Header 부 생략
    if i > 1 :
        arr.append(line.split(',')[0])
rf.close()

http = urllib3.PoolManager()

#파일 읽어서 처리 필요 있음 전에 어디 까지 처리 했는지
while True:

    for str in arr:

         r = http.request('GET',url,fields={
                                            'ServiceKey':serviceKey
                                            , 'pageNo':'1'
                                            , 'numOfRows':'500'
                                            , 'dataType':'JSON'
                                            , 'dataCd':'ASOS'
                                            , 'dateCd':'HR'
                                            , 'startDt':'20190901'
                                            , 'startHh':'00'
                                            , 'endDt':'20200110'
                                            , 'endHh':'23'
                                            , 'stnIds':str
                                            , 'schListCnt':'500'
                                            })
         print('pron str = ' + str)

         rData = r.data.decode('UTF-8')

         print(rData)

         if json.loads(rData)['response']['header']['resultCode']=="00":
            json_list = json.loads(rData)['response']['body']['items']['item']
            print(json_list)
            data = pandas.DataFrame.from_dict(json_list)
            wf.write(data.to_csv())

wf.close()


#http = urllib3.PoolManager()
#r = http.request('GET', url)

#r = http.request('GET',url,fields={
#                                    'serviceKey':serviceKey
#                                    , 'pageNo':'1'
#                                    , 'numOfRows':'1'
#                                    , 'dataType':'JSON'
#                                    , 'areaNo':'1100000000'
#                                    , 'time':'2017093106'
#                                    #, 'requestCode':'A20'
#                                    })

#r = http.request('GET',url,fields={
#                                    'ServiceKey':serviceKey
#                                    , 'pageNo':'1'
#                                    , 'numOfRows':'10'
#                                    , 'dataType':'JSON'
#                                    , 'dataCd':'ASOS'
#                                    , 'dateCd':'HR'
#                                    , 'startDt':'20100101'
#                                    , 'startHh':'00'
#                                    , 'endDt':'20100102'
#                                    , 'endHh':'23'
#                                    , 'stnIds':'108'
#                                    , 'schListCnt':'10'
#                                    })


#json_data = json.loads(r.data.decode('UTF-8'))

#print(json_data['body'])

#print(r.data)
#print(r.data.decode('UTF-8'))