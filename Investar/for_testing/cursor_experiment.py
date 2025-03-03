import pymysql
from pymysql import Error

try:
    # MySQL 연결 설정
    connection = pymysql.connect(
        host='localhost',
        user='root',  # 본인의 MySQL 사용자명
        password='sunghanmariadb',  # 본인의 MySQL 비밀번호
        database='INVESTAR',  # 사용할 데이터베이스명
        charset='utf8'
    )

    # 커서 생성
        with connection.cursor() as cursor:
            # DELETE 쿼리문   슈바 큰따옴표 작은 따옴표는 이래 쓰는거였
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
            cursor.execute(delete_query)
            
            # 변경사항 저장
            connection.commit()
        
        print("성공적으로 데이터가 삭제되었습니다.")

except Error as e:
    print(f"Error: {e}")

finally:
    # 연결 종료
    if connection.open:
        connection.close()
        print("MySQL 연결이 종료되었습니다.")
