from os import close
import aconfig,csv,time
from binance.client import Client
from binance.enums import *

# This is a csv writer it will get data from historical klines for backtesting 

###NOTE CHANGE THE CSV FILE FOR FUTURE USE
###NOTE CHANGE THE CSV FILE FOR FUTURE USE
###NOTE CHANGE THE CSV FILE FOR FUTURE USE
###NOTE CHANGE THE CSV FILE FOR FUTURE USE
###NOTE CHANGE THE CSV FILE FOR FUTURE USE

client = Client(aconfig.API_KEY, aconfig.API_SECRET)
# can change or create a file to input data
csvfile = open('daily.csv','w',newline='')
candlestick_writer = csv.writer(csvfile,delimiter=',')

# change this to get other bitcoin data
candlesticks = client.get_historical_klines("ETHUSDT",Client.KLINE_INTERVAL_15MINUTE,"1 Apr 2021","13 Sep,2021")


for candlestick in candlesticks:
    candlestick[0] = candlestick[0]/1000
    candlestick[0] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(candlestick[0])) 
    candlestick_writer.writerow(candlestick)
csvfile.close()