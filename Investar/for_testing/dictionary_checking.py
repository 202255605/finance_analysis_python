import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import MarketDB_codes_date_updated_final
import DBUpdater

mk = MarketDB_codes_date_updated_final.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
#df = pd.DataFrame()

contact_to_DBUpdater = DBUpdater.DBUpdater()

print(mk.codes)

for values_to_check in stocks:
    print(values_to_check)
    if values_to_check in mk.codes.values():
        print(f"{values_to_check}는 딕셔너리에 존재합니다.")
    else:
        print(f"{values_to_check}는 딕셔너리에 존재하지 않습니다.")
