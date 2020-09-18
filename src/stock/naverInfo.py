import pandas as pd
import urllib3

INDEX = '<td class="num"><span class="tah p11">'

TODAY     = 5
YESTERDAY = 10


def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    get_url(code)

def get_url(code_df):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code_df)
    #print("요청 URL = {}".format(url))
    return url

def get_price_to_dataFrame(url):
    df = pd.DataFrame();  # 결과 받아올 데이터 프레임
    for page in range(1, 5):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    return df

def get_price_to_str(url):
    return get_info_arr(url)[0]

#종가, 시가, 고가, 저가, 거래량
def get_stock_res_data(url):
    http = urllib3.PoolManager()
    req = http.request('GET', url)
    return str(req.data)

def set_parse_resData(resData):
    resData = resData.replace('\\n', '\n')
    resData = resData.replace('\\t', '')
    resData = resData.split('\n')
    return resData

def get_naverArr(resData, length=None):

    naverArr = []

    if length is None:
        length = 10  #기본 10일 처리

    for data in resData:
        #INDEX = '<td class="num"><span class="tah p11">'
        #해당 태그가 주가 관련 수치 태그
        if data.startswith(INDEX):
            #수치 태그일 경우 수치를 제외한 태그를 replace 한 후 숫자 변환 return 값에 append처리 한다.
            naverArr.append(int(data.replace(INDEX,"")[0:-12].replace(",","")))

        if length is not None:
            #naverArr에 값을 계속 대입 증가 len 함수를 이용 하여 Array Size 체크
            #check한 Array Size가 전달한 값과 같은면 for 문 break return 한다.
            if len(naverArr) == length:
                break;

    return naverArr

def get_info_arr(url):
    return get_naverArr(set_parse_resData(get_stock_res_data(url)))

def get_info_arr_cur(url):
    #오늘 날짜 5개 만 출력 5개
    #종가, 시가, 고가, 저가, 거래량
    len = 5
    return get_naverArr(set_parse_resData(get_stock_res_data(url, len)))