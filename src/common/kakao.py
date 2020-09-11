import urllib3
from selenium import webdriver

def getCode():
    #GET /oauth/authorize?client_id={app_key}&redirect_uri=http://test&response_type=code HTTP/1.1
    #Host: kauth.kakao.com

    restKey = 'ec35680abe2bc3a507a0bb672c4fabfb'

    http = urllib3.PoolManager()

    url = 'https://kauth.kakao.com/oauth/authorize'

    #/ oauth / authorize?client_id = {REST_API_KEY} & redirect_uri = {REDIRECT_URI} & response_type = code
    #HTTP / 1.1

    r = http.request('GET',url, fields={'client_id':restKey,'redirect_uri':'https://www.naver.com','response_type':'code'})
    print("? :" + r.data.decode())


    #호출 url
    #https://kauth.kakao.com/oauth/authorize?client_id=ec35680abe2bc3a507a0bb672c4fabfb&redirect_uri=https%3A%2F%2Fwww.naver.com&response_type=code
    #로그인 진행 하면 코드를 준다
    # 받은 코드 20200403
    #XSKNxeIxoB8KGyPskS2Z2h-BcunvYgPga5EUY88hISKbK9rMrdAY4lKJGTo_vXlwJ4uqJgo9cxcAAAFxPmUcng

    #### 위에는 다 무시하고 이 링크로 접속 해야 코드 발급 불편하다. 로그인 해야 하기 때문인거 같다.
    # https://kauth.kakao.com/oauth/authorize?client_id=ec35680abe2bc3a507a0bb672c4fabfb&redirect_uri=https%3A%2F%2Fwww.naver.com&response_type=code
    # https://kauth.kakao.com/oauth/authorize?client_id=ec35680abe2bc3a507a0bb672c4fabfb&redirect_uri=https%3A%2F%2Fwww.naver.com&response_type=code
def getToken():

    restKey = 'ec35680abe2bc3a507a0bb672c4fabfb'
    code = 'MdwsGRFJSHL3-n2R5BrBK2bK0Oe6yQTiIoUGfAbuQvSzSLCW0TVZxet5ECvaofJrDTOcTAorDR8AAAF0M3Aa9g'

    http = urllib3.PoolManager()

    url = 'https://kauth.kakao.com/oauth/token'

    r = http.request('GET', url,
                     fields={'grant_type': 'authorization_code', 'client_id': restKey, 'redirect_uri':'https://www.naver.com', 'code': code})

    print(r.data.decode())

def getLoginCode():
    driver = webdriver.Chrome("resource/chromedriver/85/win_chromedriver.exe")

    driver.get("https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.naver.com%26client_id%3Dec35680abe2bc3a507a0bb672c4fabfb")

    #id 입력 진행
    query = driver.find_element_by_id("id_email_2")
    query.send_keys("godori004@naver.com")

    #pw 입력 진행
    query = driver.find_element_by_id("id_password_3")
    query.send_keys("db2386")

    #login 버튼 클릭
    query = driver.find_element_by_class_name("submit")
    query.click()

    #code 가져오기
    key = driver.current_url
    code = key[key.find("code")+5:]

    return code