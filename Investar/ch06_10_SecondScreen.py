import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
#from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import MarketDB_codes_date_updated_final

mk = MarketDB_codes_date_updated_final.MarketDB()
df = mk.get_daily_price('SK하이닉스', '2020-01-02','2025-01-09',1)

ema60 = df.close.ewm(span=60).mean()
ema130 = df.close.ewm(span=130).mean() 
macd = ema60 - ema130
signal = macd.ewm(span=45).mean() 
macdhist = macd - signal

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
    macdhist=macdhist).dropna()
df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number','open','high','low','close']]

ndays_high = df.high.rolling(window=14, min_periods=1).max()      # ①
ndays_low = df.low.rolling(window=14, min_periods=1).min()        # ②
fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100  # ③
slow_d= fast_k.rolling(window=3).mean()                           # ④
df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()             # ⑤
# %k , %D 를 이용하는데
# 이때 %k는 내가 window로 사용할거라고 정한 일수에 대해 , %k = (오늘의 종가 - 정한일수 동안의 저점) / (일수 동안의 고점 - 일수동안의 저점) *100
# %D 는 {3일동안의 (해당날의 종가 - 해당날 기준 정한 일수동안의 저점) 합} / {3일동안의 (해당날 기준 정한 일수동안의 고점 - 해당날 기준 정한 일수동안의 저점)}
# 즉 %K의 의미는 WINDOW로 정한 날에 대해 그 해당날만큼 전의 기간동안의 모든 가격들(역대 저점과 역대 고점 사이의 가격구간) 중 오늘 종가의 상대적 위치
# 상승때일때 (EMA130이 증가 중이거나 , MACD가 양수 )
# 이건 그냥 적어보는 생각인데 MACD의 9일 ROLLING을 한 값이 신호선이잖아? 그러면 책에서도 그랬듯이 MACD HIST의 양/음이 중요한 것이 아니라 그 기울기가 중요한 것
# 가파르게 기울기가 올라간다? -> 최근 9일의 평균값에 비해 당일의 MACD의 값이 팍 올랐다 그 말은 최근 9일 이내의 상승분이 그 전보다 크다는 말 즉 강한 상승 모멘텀이 작용
# 가파르게 기울기가 내려간다? -> 최근 9일의 평균값에 비해 당일의 MACD의 값이 팍 내렸다 그 말은 최근 9일 이내의 하강분이 그 전보다 크다는 말 즉 강한 하강 모멘텀이 작용
#  장단기 이평선은 수렴과 발산을 반복하며 발산시에 MACD의 값의 절대값은 커질 것이며, 수렴한다면 0에가까운 값으로 수렴할 것이다. 그렇기에 MACD는0을 기준으로 오르내리락할 것이다.

print(df)

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - Second Screen (SK-HYNIX)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')
p1 = plt.subplot(2, 1, 2)
plt.grid(True)
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['fast_k'], color='c', label='%K')
plt.plot(df.number, df['slow_d'], color='k', label='%D')
plt.yticks([0, 20, 80, 100]) # ⑥
plt.legend(loc='best')
plt.show()
