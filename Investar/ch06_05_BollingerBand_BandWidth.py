import matplotlib.pyplot as plt
import MarketDB_codes_date_updated_final

mk = MarketDB_codes_date_updated_final.MarketDB()
df = mk.get_daily_price('NAVER', '2019-01-02','2025-01-02',1)
  

#df = mk.get_daily_price('NAVER', '2019-01-02')
df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['bandwidth'] = (df['upper'] - df['lower']) / df['MA20'] * 100 # ①
df = df[19:]

print('df생성 완료')

plt.figure(figsize=(9, 8))
plt.subplot(2, 1, 1)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
print('볼린저 밴드 그리기 완료')
print(type(df.index))
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
#print('fill between 문제 아닙니')
plt.title('NAVER Bollinger Band(20 day, 2 std)')
plt.legend(loc='best')
plt.subplot(2, 1, 2)
plt.plot(df.index, df['bandwidth'], color='m', label='BandWidth') # ②
plt.grid(True)
plt.legend(loc='best')
plt.show()
