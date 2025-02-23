from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# 옵션값 설정
opt = webdriver.ChromeOptions()
opt.add_argument('headless')

# 웹드라이버를 통해 네이버 금융 ETF 페이지에 접속
drv = webdriver.Chrome('C:\myPackage\chromedriver.exe', options=opt)
drv.implicitly_wait(3)

'''

drv.implicitly_wait(3)는 Selenium 웹 드라이버에서 사용되는 메서드로, 
드라이버가 웹 요소를 찾을 때 최대 3초 동안 대기하도록 설정하는 것입니다. 

이 메서드는 웹 페이지의 요소가 로드될 때까지 기다리도록 하여, 
요소가 아직 DOM에 존재하지 않을 경우 발생할 수 있는 NoSuchElementException을 방지하는 데 도움을 줍니다.

'''
drv.get('https://finance.naver.com/sise/etf.nhn')

# 뷰티풀 수프로 테이블을 스크래핑
bs = BeautifulSoup(drv.page_source, 'lxml')
drv.quit()
table = bs.find_all("table", class_="type_1 type_etf")
df = pd.read_html(str(table), header=0)[0]

# 불필요한 열과 행을 삭제하고 인덱스를 재설정해서 출력
df = df.drop(columns=['Unnamed: 9'])
df = df.dropna()
df.index = range(1, len(df)+1)
print(df)

# 링크 주소에 포함된 종목코드를 추출하여 전체 종목코드와 종목명 출력
etf_td = bs.find_all("td", class_="ctg")
etfs = {}
for td in etf_td:
    s = str(td.a["href"]).split('=')
    code = s[-1]
    etfs[td.a.text] = code
print("etfs :", etfs)


'''
동적 페이지에서 데이터를 추출하기 위해서는 추출하고자 하는 데이터의 html이 갱신되는데 필요한 동작을 실행시켜줘야 한다.

파이썬을 통해 동작을 자동으로 실행 시키기 위해서는 2가지가 필요하다. 동작 자동화 주문 셀레니움과 웹 제어도구 웹 드라이버이다.

셀리네움으로 동작을 지시하면 웹 드라이버에서 동작을 수행하는 것이다.

셀리네움으로 동작을 지시사면 웹 드라이버가 마치 사람인양 그런 동작들을 수행하면서 결과값을 반환해준다

'''