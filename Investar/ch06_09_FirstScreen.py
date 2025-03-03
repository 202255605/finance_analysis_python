import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
#from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import MarketDB_codes_date_updated_final

mk = MarketDB_codes_date_updated_final.MarketDB()
df = mk.get_daily_price('SK하이닉스', '2020-01-02','2025-01-09',1)

ema60 = df.close.ewm(span=60).mean()   # ① 종가의 12주 지수 이동평균
ema130 = df.close.ewm(span=130).mean() # ② 종가의 12주 지수 이동평균
macd = ema60 - ema130                  # ③ MACD선
signal = macd.ewm(span=45).mean()      # ④ 신호선(MACD의 9주 지수 이동평균)
macdhist = macd - signal               # ⑤ MACD 히스토그램

print(df)
# print(df.index) 다른 파일에서 지정한 이 df의 인덱스는 date이고
# df['number']을 밑에서 출력해보면 또 알겠지만
# -> matplotlib가 어떤 년-월-일 형식의 데이터를 자기만의 해시함수? 같은걸 이용해서 float형의 단일숫자로 바꿔버린다
print('\n\n')

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
    macdhist=macdhist).dropna() 
df['number'] = df.index.map(mdates.date2num)  
ohlc = df[['number','open','high','low','close']]

print("기존의 인덱스에 df.index.map(mdates.date2num) 을 적용한 df--> \n\n");print(df)

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - First Screen (SK-HYNIX)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', 
    colordown='blue')  # 이거 자체를 불러왔구나 ㅋㅋ mpl_finance.candlestick_ohlc도 아니고 
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')

p2 = plt.subplot(2, 1, 2)
plt.grid(True)
p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
plt.plot(df.number, df['macd'], color='b', label='MACD')
plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
plt.legend(loc='best')
plt.show()


"""
MACD 선:

일반적으로 12일 지수 이동 평균(EMA)에서 26일 EMA를 뺀 값으로 계산됩니다.

​macd = ema12 -ema26

신호선:

MACD 선의 9일 EMA로 계산됩니다.

신호선은 MACD 선의 변화를 부드럽게 하여 매매 신호를 제공하는 역할을 합니다.

MACD 선과 신호선의 해석

1. MACD 선이 신호선 위에 있을 때 (MACD > 신호선)
의미: 상승 모멘텀
해석: MACD 선이 신호선 위에 있을 때는 단기 이동 평균이 장기 이동 평균보다 높다는 것을 의미합니다. 이는 상승세가 강하다는 신호로 해석되며, 매수 신호로 간주될 수 있습니다.

2. MACD 선이 신호선 아래에 있을 때 (MACD < 신호선)
의미: 하락 모멘텀
해석: MACD 선이 신호선 아래에 있을 때는 단기 이동 평균이 장기 이동 평균보다 낮다는 것을 의미합니다. 이는 하락세가 강하다는 신호로 해석되며, 매도 신호로 간주될 수 있습니다.
MACD 선의 기울기 변화

1. MACD 선이 가파르게 증가할 때
의미: 강한 상승 모멘텀
해석: MACD 선이 가파르게 증가하면 가격 상승의 속도가 빨라지고 있다는 것을 의미합니다. 이는 강한 매수세가 작용하고 있음을 나타내며, 추가적인 상승이 예상될 수 있습니다.

2. MACD 선이 가파르게 감소할 때
의미: 강한 하락 모멘텀
해석: MACD 선이 가파르게 감소하면 가격 하락의 속도가 빨라지고 있다는 것을 의미합니다. 이는 강한 매도세가 작용하고 있음을 나타내며, 추가적인 하락이 예상될 수 있습니다.

요약
MACD > 신호선: 상승 모멘텀, 매수 신호
MACD < 신호선: 하락 모멘텀, 매도 신호
MACD 선의 가파른 증가: 강한 상승세, 추가 상승 가능성
MACD 선의 가파른 감소: 강한 하락세, 추가 하락 가능성

"""
