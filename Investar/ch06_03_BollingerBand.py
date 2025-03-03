import matplotlib.pyplot as plt
import MarketDB_codes_date_updated_final

mk = MarketDB_codes_date_updated_final.MarketDB()
df = mk.get_daily_price('NAVER', '2019-01-02','2025-01-02',1)
  
df['MA20'] = df['close'].rolling(window=20).mean()  # mean-active-line of 20 days , rolling에 min을 안 잡았음 -> 19째 days까지는 Nan 
df['stddev'] = df['close'].rolling(window=20).std() # std는 표준편차 20일마다 당연히 표준편차의 값도 바뀌겠네
df['upper'] = df['MA20'] + (df['stddev'] * 2)   # ③ 이것도 20일동안 같은 것이 아니라 계속 바뀌겠네 매일 -> 매일 평균값과 표준편차의 값이 계속 바뀔테니까
df['lower'] = df['MA20'] - (df['stddev'] * 2)   # ④
df = df[19:]  # ⑤
    
plt.figure(figsize=(9, 5))
plt.plot(df.index, df['close'], color='#0000ff', label='Close')    # ⑥
plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')       # ⑦
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')  # ⑧ 
plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day pius or minus 2 std)')
plt.show()
