
# 이건 api 형식의 파일입니다 즉 이 파일을 직접 실행 시키는 것이 아니라 특정객체 = MarketDB() 형식으로 생성하고 그 특정객체에 대해
# get_comp_info 를 실행해 회사 목록에 대한 딕셔너리를 만든 후 get_daily_info를 실행해 내가 원하는 회사코드나 회사명을 넣어 그 회사의 주식 값을 받아 오시면 된다.

# 처음 이 파일을 실행했을때 인터프리팅이 완료되고 이 파일의 실행창에는 아무것도 뜨지 않을거다 그리고 새로운 >>> 기호가 나오면 MarketDB객체를 생성해 함수를 실행하시면 된다
# 데이터베이스에도 알아서 접근이 될 테니까

import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
import re

class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root', 
            password='sunghanmariadb', db='INVESTAR', charset='utf8')
        self.codes = {}
        self.get_comp_info() # 여기 있구먼 그냥 객체 생성만 해도 회사 정보에 대한 목록은 업로드가 되는구먼
        
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes에 저장"""
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql, self.conn)
        for idx in range(len(krx)):
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]
        #print(self.codes)

    def get_daily_price(self, code, start_date=None, end_date=None , token = None):
        # 똑같이 MarKetDB를 사용한다고 불러온다고 해도 token을 안주면 2000개 정도 회사의 10일 정도 저장되어 있는 데이터를 불러오고
        # token을 주며 MarketDB의 get_daily_price를 호출하면 4개의 회사에 대해 1000개 즉 한 4년 ~ 5년 정도 되는 데이터가 불러와진다.
        """KRX 종목의 일별 시세를 데이터프레임 형태로 반환
            - code       : KRX 종목코드('005930') 또는 상장기업명('삼성전자')
            - start_date : 조회 시작일('2020-01-01'), 미입력 시 1년 전 오늘
            - end_date   : 조회 종료일('2020-12-31'), 미입력 시 오늘 날짜
        """
        if start_date is None:
            one_year_ago = datetime.today() - timedelta(days=365)
            start_date = one_year_ago.strftime('%Y-%m-%d')
            print("start_date is initialized to '{}'".format(start_date))
        else:
            start_lst = re.split('\D+', start_date)
            if start_lst[0] == '':
                start_lst = start_lst[1:]
            start_year = int(start_lst[0])
            start_month = int(start_lst[1])
            start_day = int(start_lst[2])
            if start_year < 1900 or start_year > 2200:
                print(f"ValueError: start_year({start_year:d}) is wrong.")
                return
            if start_month < 1 or start_month > 12:
                print(f"ValueError: start_month({start_month:d}) is wrong.")
                return
            if start_day < 1 or start_day > 31:
                print(f"ValueError: start_day({start_day:d}) is wrong.")
                return
            start_date=f"{start_year:04d}-{start_month:02d}-{start_day:02d}"
            print('\nstart_date is '+ start_date)

        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            print("\nend_date is initialized to '{}'".format(end_date))
        else:
            end_lst = re.split('\D+', end_date)
            # 숫자가 아닌 문자나 기호들을 싸그리 다 end_lst[0]로 묶어서 제거하고 깔끔하게 end_lst[1]로 설정
            if end_lst[0] == '':
                end_lst = end_lst[1:] 
            end_year = int(end_lst[0])
            end_month = int(end_lst[1])
            end_day = int(end_lst[2])
            if end_year < 1800 or end_year > 2200:
                print(f"ValueError: end_year({end_year:d}) is wrong.")
                return
            if end_month < 1 or end_month > 12:
                print(f"ValueError: end_month({end_month:d}) is wrong.")
                return
            if end_day < 1 or end_day > 31:
                print(f"ValueError: end_day({end_day:d}) is wrong.")
                return
            end_date = f"{end_year:04d}-{end_month:02d}-{end_day:02d}"
            print('end_date is ' + end_date)
         
        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())
        #print(codes_keys[:30])
        #print(codes_values[:30])
        print('\ncodes_keys , codes_values 안정적 업로드 완료...')

        if code in codes_keys:
            print('\nconfirm that code in codes_keys - it\'s number')
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            print('\nconfirm that code in codes_values - it\'s not number ')
            code = codes_keys[idx]
        else:
            print(f"ValueError: Code({code}) doesn't exist.")
        if token is None:
            sql = f"SELECT * FROM daily_price WHERE code = '{code}'"\
                f" and date >= '{start_date}' and date <= '{end_date}'"
        else:
            sql = f"SELECT * FROM Efficient_Frontier_line WHERE code = '{code}'"\
                f" and date >= '{start_date}' and date <= '{end_date}'"
        print('the sended query is '+ sql)
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        #print(df[:30]) -> for test
        return df 
