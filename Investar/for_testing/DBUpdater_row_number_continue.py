
import pymysql

class DBUpdater_row_number_continue:

    def __init__(self):

        self.conn = pymysql.connect(host='localhost', user='root',
            password='sunghanmariadb', db='INVESTAR', charset='utf8')

        with self.conn.cursor() as curs:
            sql = ( 'DELETE FROM daily_price'
                    'USING daily_price'
                    'INNER JOIN ('
                    'SELECT code, date,'
                    'ROW_NUMBER() OVER (PARTITION BY code ORDER BY date DESC) as row_num'
                    'FROM daily_price'
                    ') AS d2'
                    'ON daily_price.code = d2.code AND daily_price.date = d2.date'
                    'WHERE d2.row_num > 10;'
                   # 그래 파이썬에서는 들여쓰기가 그 어떤 것보다도 중요했었다 -> 이 따옴표 있는 문장도 들여쓰기를 맞춰서 했어야 했는
                   ) # 아 구문같은거 줄바꿈문자 졸라 써야해서 실었는데 이렇게 간단히 처리가 된다. 
            curs.execute(sql)
            
        self.conn.commit()

if __name__ == '__main__':  # 직접 실행된다면 이렇게 이 파일 객체의 인스턴스로 만들어서 작동하도록 설
    dbu = DBUpdater_row_number_continue()
