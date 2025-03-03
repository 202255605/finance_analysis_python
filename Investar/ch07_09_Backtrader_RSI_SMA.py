import backtrader as bt
from datetime import datetime
import yfinance as yf

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        
        """
            data = bt.feeds.PandasData(dataname=df)를 통해 data 객체를 생성하고, cerebro.adddata(data)를 호출하면, cerebro는 이 데이터를 내부적으로 처리하여 self.datas와 self.data에 저장합니다.

        self.datas:

        self.datas는 추가된 모든 데이터 피드를 포함하는 리스트입니다. 이 경우, data 피드가 추가되므로 self.datas는 다음과 같은 형태가 됩니다:

        self.datas = [data]
        self.datas[0]는 data 피드를 가리킵니다. --> 아 data라는 데이터프페임이던 뭐던 어쨋든 이 객체가 리스트에 담겨서 전달되는 구나 그래서 self.datas[0]이라는 표현을 쓰는구나
        self.data:

        self.data는 기본 데이터 피드를 가리키며, 일반적으로 self.datas[0]와 동일합니다. 따라서, self.data는 data 피드를 가리키게 됩니다.
        """
        self.order = None
        self.buyprice = None
        self.buycomm = None    # 일단 실제 값은 없는 채로 생성    
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def notify_order(self, order):  # ①
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:  # ② 
            if order.isbuy():
                self.log(
                    f'BUY  : 주가 {order.executed.price:,.0f}, '
                    f'수량 {order.executed.size:,.0f}, '
                    f'수수료 {order.executed.comm:,.0f}, '        
                    f'자산 {cerebro.broker.getvalue():,.0f}'
                    ) 
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else: 
                self.log(
                    f'SELL : 주가 {order.executed.price:,.0f}, '
                    f'수량 {order.executed.size:,.0f}, '
                    f'수수료 {order.executed.comm:,.0f}, '
                    f'자산 {cerebro.broker.getvalue():,.0f}'
                    ) 
            self.bar_executed = len(self)
            print(self.bar_executed)
            # 딱 알았음 self.bar_executed를 출력 하면 알겠지만 backtrader은 그냥 자신에게 들어온 금융데이터프레임에 대해 모든 행 즉 모든 datetime에 따라
            # def next(self)를 수행하고 바로 notify_order수행 그리고 notify_order의 수행 중에 있는 self.log의 함수는 뭐 def log(self,txt,dt = None) 로 정의되어 있고
            # self.bar_executed는 내장 변수인 self를 바로 받는 값으로 자신이 수행을 완료한 행의 수를 저장하는 듯 -> 그래서 주문이 들어갔을때 같이 출력되는 self.bar_executed를 보면
            # 수가 몇십씩 늘어나 있음
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELD')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None #self.order은 초기화  

    def next(self):
        if not self.position:
            if self.rsi < 40:
                self.order = self.sell()
            elif self.rsi <30:
                self.order = self.buy()
                # 사실 매번 next 함수에서 self.order을 None으로 초기화 하고 그 값이 None에서 바뀐다면 self.buy() , self.sell()밖에 없으니 cancel,margin,reject는
                # 수행될 일이 없군
        else:
            if self.rsi > 70:
                self.order = self.buy()
            elif self.rsi >90:
                self.order = self.sell()

    def log(self, txt, dt=None):  # ③ 
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')
        # 결과는 이런 식
        #[2018-03-02] BUY  : 주가 345,056, 수량 26, 수수료 12,432, 자산 10,083,568,282

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
tick = 'AAPL' # 회사명 맘대
df = yf.download(tick, start='2023-01-01', end='2025-01-01')
# YahooFinanceData 내가 작동 안 될 줄 알았음 예전에도 그랬거든
print(df)
df.reset_index(inplace=True)
# Pandas 데이터프레임에서 인덱스를 리셋하고, 기존 인덱스를 새로운 열로 추가하는 기능을 수행합니다.
#inplace=True를 사용하면 원본 데이터프레임이 수정됩니다.
# print(df) 또는 print(df.columns)를 하면 딱 알겠지만 backtrader가 딱 받을 수 있게 형식화된 column들과
#이름도 다르고 계다가 1차원 column도 아니고 multi_column으로 2차원 column으로 나온다

df.columns = ['_'.join(col).strip() for col in df.columns.values]
# MultiIndex를 평탄화합니다.

# 필요한 열만 선택하고, 열 이름을 Backtrader에서 기대하는 형식으로 변경합니다.
#--> 왜냐면 backtrader 이 받고자 하는 방식으로만 받을 수 있거든요

closetick = 'Close_'+tick
hightick ='High_'+tick
lowtick ='Low_'+tick
opentick ='Open_'+tick
volumetick ='Volume_'+tick

df = df.rename(columns={
    'Date_': 'datetime',
    closetick: 'close',
    hightick: 'high',
    lowtick: 'low',
    opentick: 'open',
    volumetick: 'volume'
})

# datetime 열을 인덱스로 설정합니다.
df.set_index('datetime', inplace=True)

print("인덱스를 변환한 데이터 프레임 \n\n");print(df);

# 이제 Backtrader에 사용할 수 있습니다.--> backtrader이 가지고 놀 데이터셋을 선물 받았습니다
data = bt.feeds.PandasData(dataname=df)

cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission=0.0014)  # ④
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)  # 

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot(style='candlestick')  # ⑥
