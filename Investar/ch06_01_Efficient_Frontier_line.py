import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import MarketDB_codes_date_updated_final
import DBUpdater

mk = MarketDB_codes_date_updated_final.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()

#여기는 데이터베이스에 데이터 넣기
"""contact_to_DBUpdater = DBUpdater.DBUpdater()  // 아 ㅋㅋ 내가 2개 객체의 인스턴스를 각각 만들어 줬었구

contact_to_DBUpdater.codes = {key: value for key, value in mk.codes.items() if value in ['삼성전자','SK하이닉스','현대자동차','NAVER']}

print('contact_to_DBUpdater.codes is ') ; print(contact_to_DBUpdater.codes); print('\n');

contact_to_DBUpdater.update_daily_price(100 , 1) # 1은 token"""

#여기서부터가 데이터베이스에 있는 데이터 불러오기
for s in stocks:
    df[s] = mk.get_daily_price(s, '2020-12-16', '2024-01-09' ,1 )['close'] # 인자 자리의 1은 token -> 참조하는 테이블이 efficient_Frontier_line테이블
    # 그래프 출력을 위한 입력데이터 양의 조절은 여기서 마음대로 기간을 설정하면서 바꾸면 된다.
    print('여기서 출력')
    print(df[s])

  
daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
print('annual_ret의 자료형은'); print(type(annual_ret)); # 확인했는데 series네
daily_cov = daily_ret.cov() 
annual_cov = daily_cov * 252

port_ret = [] 
port_risk = [] 
port_weights = [] 

for _ in range(20000): 
    weights = np.random.random(len(stocks)) 
    weights /= np.sum(weights) 

    returns = np.dot(weights, annual_ret)  # 2차원 벡터, 2차원 벡터의 내적 -> 1차원 벡터 즉 스칼라값의 반한
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
    # 2차원 벡터 , 2차원 행렬의 내적 -> 2차원 벡터 즉 '배열' 값의 반환 후 2차원 벡터끼리의 내적 즉 스랄라값의 반환

    port_ret.append(returns) 
    port_risk.append(risk) 
    port_weights.append(weights) 

portfolio = {'Returns': port_ret, 'Risk': port_risk} 
for i, s in enumerate(stocks): 
    portfolio[s] = [weight[i] for weight in port_weights] 
df = pd.DataFrame(portfolio) 
df = df[['Returns', 'Risk'] + [s for s in stocks]]
print(df)


df.plot.scatter(x='Risk', y='Returns', figsize=(8, 6), grid=True)
plt.title('Efficient Frontier') 
plt.xlabel('Risk') 
plt.ylabel('Expected Returns') 
plt.show() 
