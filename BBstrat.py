import backtrader as bt
from backtrader.indicators import ema
import time
import talib
from talib import MA_Type
### READ B4 TESTING 
### FAILED STRAT IS COMMENTED
### HIGHEST SCORE : 0.932991 /// BBANDS OR RSI

### HIGHEST SO FAR : 14/9/2021
### SHARPE RATIO OF 1.97 USING BBSTRAT PERIOD = 80 AND A TRAILING STOPLOSS DATE FROM "1 Jan 2021","13 Apr,2021"



class BBand(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        self.bbands = bt.ind.BollingerBands(self.datas[0], period=800)
        self.buysig = bt.indicators.CrossOver(self.datas[0], self.bbands.lines.bot)
        self.sellsig = bt.indicators.CrossOver(self.datas[0], self.bbands.lines.top)
        self.roc = bt.indicators.RateOfChange(self.datas[0],period =800)
        self.dataclose = self.datas[0].close
        self.rsi = bt.indicators.RSI_SMA(self.dataclose, period=25)
        self.order = None
        self.buyprice = None
        self.buycomm = None
        ###INDICATORS FOR FUN
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
            # if self.buysig < 0 or self.rsi > 70 : ##self.crossover gives bad sharpe
            if self.buysig> 0 :  ##or self.rsi>70
                self.order = self.buy()
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.boughtprice = self.dataclose[0]

                

        else:
        
            # if self.sellsig > 0 or self.rsi < 30:
            if self.sellsig < 0:
                self.order = self.sell()
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

            ## Create Stop loss
            self.stoploss = self.boughtprice - (self.boughtprice*0.3)

            if self.dataclose[0] < self.stoploss:
                self.order = self.sell()
                self.log('STOP LOSS INITIATED, %.2f' % self.dataclose[0])
                


