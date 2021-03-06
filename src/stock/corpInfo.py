import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt

# 종목 타입에 따라 download url이 다름. 종목코드 뒤에 .KS .KQ등이 입력되어야해서 Download Link 구분 필요
stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}


# 회사명으로 주식 종목 코드를 획득할 수 있도록 하는 함수
def get_code(df, name):

    tmp = df.query("name=='{}'".format(name))

    if tmp.size < 1:
        print("코드값 이 없습니다. 에러 발생")
        raise Exception

    code = tmp['code'].to_string(index=False)

    # 위와같이 code명을 가져오면 앞에 공백이 붙어있는 상황이 발생하여 앞뒤로 sript() 하여 공백 제거
    code = code.strip()
    return code


# download url 조합
def get_download_stock(market_type=None):

    market_type_param = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type_param

    df = pd.read_html(download_link, header=0)[0]
    return df
#https://finance.naver.com/item/sise_day.nhn?code=234340
#https://finance.naver.com/item/sise_day.nhn?code=234340

# kospi 종목코드 목록 다운로드
def get_download_kospi():

    df = get_download_stock('kospi')
    df.종목코드 = df.종목코드.map('{:06d}.KS'.format)

    return df

# kosdaq 종목코드 목록 다운로드
def get_download_kosdaq():

    df = get_download_stock('kosdaq')
    df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)

    return df

def get_concat_corpInfo(kospi_df, kosdaq_df):

    pdData = pd.concat([kospi_df, kosdaq_df])

    pdData = pdData[['회사명', '종목코드', '업종']]

    ######추후 수정 필요
    addData = [('동양물산', '002900.KQ', '')]
    # Create a DataFrame object
    pAddData = pd.DataFrame(addData, columns=['회사명', '종목코드', '업종'])

    pdData = pd.concat([pdData, pAddData])
    #########
    pdData = pdData.rename(columns={'회사명': 'name', '종목코드': 'code', '업종': 'sector'})
    pdData = pdData.fillna('-')
    return pdData

def get_kospi_kosdaq_dataFrame():
    return get_concat_corpInfo(get_download_kospi(), get_download_kosdaq())

def getMyStockInfoNmCdDict(pdData, stockNameArr):

    rtnDict =   {}

    for name in stockNameArr:
        rtnDict[name] = get_code(pdData, name)[0:-3]

    return rtnDict

