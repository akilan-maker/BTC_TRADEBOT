import backtrader as bt
from backtrader.indicators import ema
import time

### READ B4 TESTING 
### FAILED STRAT IS COMMENTED
### HIGHEST SCORE : 0.932991 /// BBANDS OR RSI


class hrstrat(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    params =  (
        # Standard MACD Parameters
        ('macd1', 12),
        ('macd2', 26),
        ('macdsig', 9),
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist', 3.0),   # ATR distance for stop price
        ('smaperiod', 30),  # SMA Period (pretty standard)
        ('dirperiod', 10),  # Lookback period to consider SMA trend direction
        ('ema',4000),
        ('atrperiod',1000)
    )

    def __init__(self):
        self.bbands = bt.ind.BollingerBands(self.datas[0], period=25)
        self.buysig = bt.indicators.CrossOver(self.datas[0], self.bbands.lines.bot)
        self.sellsig = bt.indicators.CrossOver(self.datas[0], self.bbands.lines.top)
     
        # self.macd = bt.indicators.MACD(self.data,
        #                                period_me1=self.p.macd1,
        #                                period_me2=self.p.macd2,
        #                                period_signal=self.p.macdsig)

        # # Cross of macd.macd and macd.signal
        # self.mcross = bt.indicators.CrossOver(self.macd.macd, self.macd.signal)
        # # Control market trend
        # self.sma = bt.indicators.SMA(self.data, period=self.p.smaperiod)
        # self.smadir = self.sma - self.sma(-self.p.dirperiod)
        self.dataclose = self.datas[0].close
        self.rsi = bt.indicators.RSI_SMA(self.dataclose, period=15)
        self.order = None
        self.buyprice = None
        self.buycomm = None

        sma1 = bt.indicators.SMA(period = 200)##fast
        sma2 = bt.indicators.SMA(period = 500)##slow     
        self.crossover = bt.indicators.CrossOver(sma1,sma2)

        ## THIS IS KETLER CHANNEL
        # self.basis = bt.indicators.EMA(self.data, period=self.p.ema)
        # atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)
        # self.upper = self.basis + 2 * atr
        # self.lower = self.basis - 2 * atr
        ## https://community.backtrader.com/topic/1720/custom-indicator




        ###INDICATORS FOR VIEW
        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0]).plot = False



    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        self.order =None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):

        # self.log('Close %.2f' % self.dataclose[0])
        if self.order:
            return
        if not self.position:
            
            if   self.crossover > 0:
                self.order = self.buy()
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # if self.mcross[0] >0.0 or self.smadir <0.0: #macd and sma
            #     self.order = self.buy()
            #     self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # if self.buysig < 0:
            #    self.order = self.buy()
            #    self.log('BUY CREATE, %.2f' % self.dataclose[0])
            
            ## use keltner channels and macd
            # if self.upper<0:
            #    self.order = self.buy()
            #    self.log('BUY CREATE, %.2f' % self.dataclose[0])
            


        else:
            if self.position:
        
            # if self.sellsig > 0 or self.rsi < 30:
            # if   self.rsi > 70 or self.sellsig > 0 :
            #     self.order = self.sell()
            #     self.log('SELL CREATE, %.2f' % self.dataclose[0])
                if   self.crossover < 0 or self.rsi>70: # or self.rsi >70 :
                    self.order = self.sell()
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])
            

            ###SELF.RSI >70 IS OUR STOP LOSS

                # if self.lower > 0:
                #     self.order = self.sell()
                #     self.log('SELL CREATE, %.2f' % self.dataclose[0])
        

