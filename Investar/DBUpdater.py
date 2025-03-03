import pandas as pd
from bs4 import BeautifulSoup
import urllib, pymysql, calendar, time, json
from urllib.request import urlopen , Request
from datetime import datetime
from threading import Timer
import urllib.parse
import requests


class DBUpdater:
    
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root',
            password='sunghanmariadb', db='INVESTAR', charset='utf8')
        
        with self.conn.cursor() as curs:
            
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)
            
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)

            sql_for_Efficient_Frontier_line = """
            CREATE TABLE IF NOT EXISTS Efficient_Frontier_line (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
                
            """
            curs.execute(sql_for_Efficient_Frontier_line)
            
        self.conn.commit() # 영구적으로 접속한 DB에 이 TABLE을 만들어서 유지
        
        self.codes = dict()
               
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close() 
     
    def read_krx_code(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method='\
            'download&searchType=13' # 다운로드 차단도 수동으로 차단함 -> 안정적 다운로드 확인
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx
    
    def update_comp_info(self):
        
        
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장

        --> 종목코드와 상장법인명이 서로 바뀔일은 없지만

            그날 그날 상장폐지된 법인이 있을 수도 있고 또는 새로이 상장된 법인도 있을 수 있다

            그 정보들까지 해서 종합적으로 '상장법인코드-상장법인명'이 저장되어있는 company_info

            의 테이블을 update 시킨다.

        """
        
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]

        # db속 테이블을 딕셔너리로 옮겨닮기 --> 그래야 조작도 편하고 , 다 고치고 나서 한번에 commit시키기도 편하니까 --> 이렇게 옮겨 놓고 나중에 쓴다.
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                # 처음 실행했을때는 데이터베이스 속 테이블도 딕셔너리도 비어 있으니 rs[0] == None 이라서 사실상 여기서부터 시작
                krx = self.read_krx_code()
                for idx in range(len(krx)):  # krx도 데이터프레임
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]               
                    sql = f"REPLACE INTO company_info (code, company, last"\
                        f"_update) VALUES ('{code}', '{company}', '{today}')"
                    # 1/10에 한번 fetch가 컴퓨터 마음대로 잘못 설정되어 처음에 있는 4개 정도 회사의 daily_info가 잘못 설정됨 row가 10개씩 들어가야 하는데 이런 젠장 1000개씩 들어감
                    # 이후 나의 소스 파일이 정상적으로 실행되더라도 잘 못 더 들어온 행이 지워지지는 않는다 이미 있는 행이 REPLCE되는 것 뿐이다.
                    # 그래서 잘 못 들어온 것을 수동으로 지워야겠다.
                    curs.execute(sql)
                    self.codes[code] = company
                    # code는 krx에서 가져온 dataframe에서 낚아온 인덱스에 해당하는 상장법인코드 , 아까 db에서 꺼내와서 딕셔너리로 옮긴 self.codes라는 딕셔너리 수정
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx+1:04d} REPLACE INTO company_info "\
                        f"VALUES ({code}, {company}, {today})") # 이 부분이 cmd창에 나타나시는 부분입니다.
                self.conn.commit()
                print('')              

    def read_naver(self, code, company, pages_to_fetch ,):
        """네이버에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        # replace_into_db로 가시면 
        # 이 함수로 읽어온 특정 회사의 주식시세 데이터프레임 데이터를 한 줄씩 읽어서 sql문으로 만들어서
        # db에 보내서 db를 매일마다 새로 읽어온 시세에 맞춰 데이터베이스를 한 행씩  수정 
        try:
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}" # 이것때문에 구분이 되는군(같은 td클래스 , pgRR부분은 같지만 일별시세,시간당시세 구분에는 이 코드가 쓰임) 

            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

            req = requests.get(url , headers = headers)
            
            doc = req.text  # 네이버 금융의 경우 EUC-KR 인코딩을 사용하므로, 다음과 같이 코드를 수정하면 됩니다:

                #encoding = chardet.detect(doc_before)['encoding']
                #doc = doc_before.decode(encoding, errors='replace')  # 오류 발생 시 '?'로 대체
                # with ~ as가 문제 인듯 testing.py에서 requests로 불러왔을때는 잘만 불러와지 잖아 이제 with~as 버린다
                            
            if doc is None:
                    print('error message : doc is None')
                    return None
            html = BeautifulSoup(doc, "lxml")
            pgrr = html.find("td", class_="pgRR")
            if pgrr is None:
                    print('error message : pgrr is None')
                    return None
            s = str(pgrr.a["href"]).split('=')
            #print('여기까지 옴4')
            
            lastpage = s[-1]
            
            df = pd.DataFrame()
            pages = min(int(lastpage), pages_to_fetch)
            
            df_list = [] # append 이제 안 됩니다.
            for page in range(1, pages + 1):
                pg_url = '{}&page={}'.format(url, page)
                pg_url_packaging = requests.get(pg_url , headers={'User-agent': 'Mozilla/5.0'}).text
                df_list.append(pd.read_html(pg_url_packaging , header=0)[0])
                
                #아니 대체 왜 pd.read_html(pg_url , header = 0)[0] 로 적었더니 이상하게 encoding , decoding 문제가 생겼던거지?
                
                # 그리고 오류가 틀린말도 아닌게 네이버 금융의 데이터는 인코딩이 euc-kr로 되어 있었고 너가 url로 보낼때의 디코딩 방식은 utf-8인데 또 왜 문제 없이 잘 되는거야
                
                # 오늘의 교훈 : 지금 일어난 오류가 정말 너가 찝고 있는 그 지점에서 일어난게 맞는거야? -> 중단지점 설정의 중요성
                
                #print('append 실행')
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                #print('시간구하기 진입')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                    format(tmnow, company, code, page, pages), end="\r")
                
            df = pd.concat(df_list, ignore_index=True)
            
            #print(' 합치기 성공')

            df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'})

            #print('rename 성공')
            
            df['date'] = df['date'].replace('.', '-')

            #print('기호바꾸기 성공')
            
            df = df.dropna()

            #print('dropna 성공')

            print(df)

            df['diff'] = df['diff'].str.extract('(\d+)').astype(float)  # 숫자만 추출하고 float로 변환
            # 그래도 상승과 하락은 표현을 해주셔야 하는데

            print(df)
            
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                'diff', 'open', 'high', 'low', 'volume']].astype(int)
           # print('여기가 실패 지점 이구')
            
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df 

    def replace_into_db(self, df, num, code, company , token = None):
        """네이버에서 읽어온 주식 시세를 DB에 REPLACE"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                if(token is None):
                    sql = f"REPLACE INTO daily_price VALUES ('{code}', "\
                        f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                        f"{r.diff}, {r.volume})"
                else:
                    sql = f"REPLACE INTO Efficient_Frontier_line VALUES ('{code}', "\
                        f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                        f"{r.diff}, {r.volume})"
                curs.execute(sql)
            self.conn.commit()
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_'\
                'price [OK]'.format(datetime.now().strftime('%Y-%m-%d'\
                ' %H:%M'), num+1, company, code, len(df)))

    def update_daily_price(self, pages_to_fetch , token = None): 
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""
        # update_comp_info 함수를 거치면서 daily로 업데이트 된(회사 목록도 업데이트 , ) self.codes 라는 딕셔너리를 이용하시는거죠 ->
        # 그리고 self.codes는 인덱스-회사코드-회사이름 이렇게 구성됨
        print('4개의 쌍만 있어야 하는 dictionary')
        print(self.codes)
        print('DBUpdater.update_daily_price 함수 시작중...')
        for idx, code in enumerate(self.codes):
            print(idx,code)
            df = self.read_naver(code, self.codes[code], pages_to_fetch) # 매일마다 바뀌는 회사별 가격 데이터프레임 
            if df is None:
                print('read_naver 실패 -> 다음 실행으로 넘어갑니다')
                continue
            print('replace_into_db 실행')
            if(token is None):
                self.replace_into_db(df, idx, code, self.codes[code])
            else:
                self.replace_into_db(df, idx, code, self.codes[code],token)

    def execute_daily(self):
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""
        self.update_comp_info() # 매일마다 상장법인 목록 바뀌었는지 체크 -> update_comp_info(){company_info 테이블 수정}-> read_krx_code  , 여기서 self.codes 1차 수정
        
        try:
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                pages_to_fetch = config['pages_to_fetch']
        except FileNotFoundError:
            with open('config.json', 'w') as out_file:
                pages_to_fetch = 100 
                config = {'pages_to_fetch': 1}
                json.dump(config, out_file)

        print('update_daily_price 함수 시작')

        print(self.codes)
        
        self.update_daily_price(pages_to_fetch) # 이제 아까 바뀐 self.codes 기반으로 한 행에 해당하는 회사 하나마다 read_naver로 바뀐 시세 데이터를 dataframe으로 읽어와서
        # replace_into_db 까지 적용하여 내 마리아 db속 테이블로 저장되어 있는 회사별-가격테이블(daily_price) 하나하나를 수정
        # 솔직히 마음 같아서는 daily_price 같은 방식 말고 회사 하나하나마다의 테이블을 만들어서 한 2002년도 부터의 가격데이터를 다 때려 넣어 놓고 싶은데 그러면 서버가 하나 필요하겠죠..

        with self.conn.cursor() as curs:
            # DELETE 쿼리문
            delete_query = """
            DELETE daily_price FROM daily_price
            JOIN (
                SELECT code, date,
                ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) as row_num
                FROM daily_price
            ) d2
            ON daily_price.code = d2.code AND daily_price.date = d2.date
            WHERE d2.row_num > 10
            """
            
            # 쿼리 실행
            curs.execute(delete_query)
            
            # 변경사항 저장
            self.conn.commit()

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year+1, month=1, day=1,
                hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month+1, day=1, hour=17,
                minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day+1, hour=17, minute=0, #장 마감시간인 17시
                second=0)   
        tmdiff = tmnext - tmnow 
        secs = tmdiff.seconds
        t = Timer(secs, self.execute_daily) # 한번 나의 로컬에서 이 파일을 실행시키면 어쨋든 매일 오후 5시마다 company_info , daily_price가 알아서 계속 바뀌겠구먼 
        print("Waiting for next update ({}) ... ".format(tmnext.strftime
            ('%Y-%m-%d %H:%M'))) # window업데이트 같은거 때문에 부득이 하게 이 파이썬 파일의 실행이 종료될 수 있기에 run레지스트리 등록
        t.start()

if __name__ == '__main__':  # 직접 실행된다면 이렇게 이 파일 객체의 인스턴스로 만들어서 작동하도록 설
    dbu = DBUpdater()
    dbu.execute_daily()
