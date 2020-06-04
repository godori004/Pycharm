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

def get_naverArr(resData, len=None):
    naverArr = []
    end      = len  #총 가져올 길이 오늘 날짜만 가져오면 5

    for data in resData:
        if data.startswith(INDEX):
            naverArr.append(int(data.replace(INDEX,"")[0:-12].replace(",","")))

        if len is not None:
            if len(naverArr) == end:
                break;

    return naverArr

def get_info_arr(url):
    return get_naverArr(set_parse_resData(get_stock_res_data(url)))

def get_info_arr_cur(url):
    #오늘 날짜 5개 만 출력 5개
    #종가, 시가, 고가, 저가, 거래량
    len = 5
    return get_naverArr(set_parse_resData(get_stock_res_data(url, len)))