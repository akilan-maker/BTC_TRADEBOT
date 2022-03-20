import backtrader as bt
import datetime
from BBstrat import BBand ##want change strat change this


cerebro = bt.Cerebro()
cerebro.broker.setcash(200.0)
cerebro.addstrategy(BBand)

### SHARPE RATIO OF 1.97 USING BBSTRAT PERIOD = 80 AND A TRAILING STOPLOSS DATE FROM "1 Jan 2021","13 Apr,2021"

# ## THIS ONLY APPLIES TO YAHOO FINANCE DATA ONLY (FOR IBKR ONLY)
# data = bt.feeds.YahooFinanceCSVData(
#     dataname='XPEV.csv',
#     fromDate=datetime.datetime(2020,9,14),
#      todate=datetime.datetime(2021,9,10),
#      reverse=False)
# ################################################



### MAKE A STOP LOSS OIII


data = bt.feeds.GenericCSVData(
    dataname="daily.csv",
    datetime=0,
    high=2,
    low=3,
    open=1,
    close=4,
    volume=5,
    openinterest=-1,
    timeframe=bt.TimeFrame.Minutes,
    compression=15
)



cerebro.adddata(data)
cerebro.broker.setcommission(commission=0.001)
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
# cerebro.addanalyzer(bt.analyzers.SharpeRatio, timeframe=bt.TimeFrame.Months, compression=1,factor=365,annualize = True ,_name="mysharpe",riskfreerate=0.01)
cerebro.addanalyzer(bt.analyzers.SharpeRatio,timeframe=bt.TimeFrame.Days, compression=1,factor=365,_name="mysharpe",riskfreerate=0.01)
# cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annual')
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.addanalyzer(bt.analyzers.DrawDown)

print("Starting Portfolio value: %.2f" % cerebro.broker.getvalue())
results = cerebro.run()
result = results[0]
print('Sharpe Ratio:    %s' % result.analyzers.mysharpe.get_analysis())  
# print('Norm. Annual Return:     %.3f' % result.analyzers.returns.get_analysis())
print('Max Drawdown:     %s' % result.analyzers.drawdown.get_analysis())  
# print('Annual Ratio:     %s' % result.analyzers.annual.get_analysis())  
print("Final Portfolio value: %.2f" % cerebro.broker.getvalue())
cerebro.plot()


# Always set annualize =True, because sharpe ratio is usually in annual form.
# Set riskfreerate=0.01 and convertrate=True, Backtrader already sets them default
# Set timeframe and compression to make TimeReturn take a snapshot on equity curve per day, if the timeframe of your data feed is equal or less than 1 day, set timeframe=bt.TimeFrame.Days, compression=1, otherwise set timeframe=bt.TimeFrame.Days, compression=data_feed
# Set factor to 252 for stocks and 365 for cryptocurrencies.