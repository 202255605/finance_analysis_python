# 기존에 출력한 효율적 투자선을 뽑아내기위해 사용했던 인자들의 값을 응용해서 샤프지수의 값을 각 가중치 모음마다 새로 뽑는다
# 그러면 그 20000개의 모듈 마다 샤프지수가 뽑힌다
# 효율적투자선 위라는 포지션에서 각 위험당 수익율이 가장 높은 지점을 빨간마커로 표시한다
# 또한 이건 좀 단순하긴한데 위험률이 가장 낮은 지점또한 표시한다.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import MarketDB_codes_date_updated_final
import DBUpdater

mk = MarketDB_codes_date_updated_final.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()

#여기는 데이터베이스에 데이터 넣기
"""contact_to_DBUpdater = DBUpdater.DBUpdater()

contact_to_DBUpdater.codes = {key: value for key, value in mk.codes.items() if value in ['삼성전자','SK하이닉스','현대자동차','NAVER']}

print('contact_to_DBUpdater.codes is ') ; print(contact_to_DBUpdater.codes); print('\n');

contact_to_DBUpdater.update_daily_price(100 , 1) # 1은 token """

#여기서부터가 데이터베이스에 있는 데이터 불러오기
for s in stocks:
    df[s] = mk.get_daily_price(s, '2020-12-16', '2023-01-09' ,1 )['close'] # 인자 자리의 1은 token -> 참조하는 테이블이 efficient_Frontier_line테이블
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
sharp_ratio = []

for _ in range(20000): 
    weights = np.random.random(len(stocks)) 
    weights /= np.sum(weights) 

    returns = np.dot(weights, annual_ret)  # 2차원 벡터, 2차원 벡터의 내적 -> 1차원 벡터 즉 스칼라값의 반한
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))
    # 2차원 벡터 , 2차원 행렬의 내적 -> 2차원 벡터 즉 '배열' 값의 반환 후 2차원 벡터끼리의 내적 즉 스랄라값의 반환

    port_ret.append(returns) 
    port_risk.append(risk) 
    port_weights.append(weights)
    sharp_ratio.append(returns/risk)

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe':sharp_ratio}
#key는 비율명이고 #value는 책에 있는 데이터프레임 사진을 보면 더 잘 이해가 되겠지만 , 각 column들에 해당하는데이터들을 모아놓은 20000개의 인덱스를 가지는 배열

for i, s in enumerate(stocks): 
    portfolio[s] = [weight[i] for weight in port_weights] # port_weights은 2차원 배열이고, 그 2차원배열을 한 행씩 슬라이스하고 각 주식명 마다의 비율을 회전에서 데이터프레임에 부착

df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk','Sharpe'] + [s for s in stocks]]
print(df)
max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]
print('max_sharpe의 타입은' ); print(type(max_sharpe));
min_risk = df.loc[df['Risk'] == df['Risk'].min()]
print('min_risk의 타입은' ); print(type(min_risk));

df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
    #c='Sharpe': 각 점의 색상을 'Sharpe'라는 열의 값에 따라 설정합니다. -> c='b'그냥 이렇게 했다면 점의 색을 파란색으로 설정했겠지만 df의 변수이기 때문에 그 변수의 값에 따라 그 점의 색을
    # 설정한다 이 정도로 생각하면 될 듯 #이 열은 각 포트폴리오의 샤프 비율을 포함하고 있어야 하며, 색상은 포트폴리오의 성과를 시각적으로 나타내는 데 사용됩니다
    #cmap='viridis':색상 맵(color map)을 'viridis'로 설정합니다.
    #'viridis'는 색상 변화가 잘 보이는 색상 맵으로, 데이터의 값에 따라 색상이 변합니다.색상맵이라는 건 검색해보면 알겠지만 수치에 따라 그 색상이 변하는 기준막대? 같은거다
    # 색상맵에는 여러 종류가 있는데 한글에 적어놓겠다ㅣ 
    edgecolors='k', figsize=(11,7), grid=True)  # ⑤
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r', 
    marker='*', s=300)  # s는 무엇일까 -> 찍힐 점의 크기를 말하며 default는 200이다 즉 여기서는 찍히는 별의 크
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r', 
    marker='X', s=200)  
plt.title('Portfolio Optimization') 
plt.xlabel('Risk') 
plt.ylabel('Expected Returns') 
plt.show()
