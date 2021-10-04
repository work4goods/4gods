import json
import random as rand
from time import sleep
import schedule
from datetime import datetime
import calendar
from kucoin.client import Client
from random import randrange
from tradingview_ta import TA_Handler, Interval, Exchange
from datetime import datetime
import calendar


import json
import random
import schedule
import time
from time import sleep
from kucoin.client import Client
from random import randrange
from tradingview_ta import TA_Handler, Interval, Exchange

strategy = TA_Handler(
    symbol="",
    screener="",
    exchange="",
    interval=Interval.INTERVAL_1_DAY
) #future dev


api_key = ''
api_secret = ''
api_passphrase = ''

client = Client(api_key, api_secret, api_passphrase)
clientMM1 = Client('', '', '')
clientMM2 = Client('', '', '')
clientPrice = Client('', '', '')
clientSpread = Client('', '', '')

ticker = clientPrice.get_ticker('GMB-USDT')
ticker1 = clientPrice.get_ticker('BTC-USDT')
ticker2 = clientPrice.get_ticker('ETH-USDT')


#insufficient funds
clientMM1 = Client('', '', '')
clientMM2 = Client('', '', '')
print('Started Trading')
#get clients
account1 = clientMM1.get_account('')
account2 = clientMM1.get_account('')
account3 = clientMM1.get_account('')
account4 =  clientMM1.get_account('')
bitcoinMM1 = account4['available']
ethereumMM1 = account3['available']
tetherMM1 = account1['available']
gambMM1 = account2['available']
account1 = clientMM2.get_account('')
account2 = clientMM2.get_account('')
account3 = clientMM2.get_account('')
account4 =  clientMM2.get_account('')
bitcoinMM2 = account4['available']
ethereumMM2 = account3['available']
tetherMM2 = account1['available']
gambMM2 = account2['available']

if(float(tetherMM1) + float(tetherMM2) < 999.99):
    print('not enough tether calling spread')
    need = 1000.99 - (float(tetherMM1) + float(tetherMM2))
    ticker = clientSpread.get_ticker('GMB-USDT')
    amount = str(int(need / float(float(ticker['price']))))
    if(int(amount) < 1000):
        amount = '1000'
    if(float(tetherMM1) < float(tetherMM2)):
        order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_SELL, ticker['price'], amount) #place to sell
        clientSpread.create_market_order('GMB-USDT', Client.SIDE_BUY, client_oid = order['orderId'], size=int(amount)) #buying it
        print('Spread helps')
    else:
        order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_SELL, ticker['price'], amount) #place to sell
        clientSpread.create_market_order('GMB-USDT', Client.SIDE_BUY, client_oid = order['orderId'], size=int(amount)) #buying it
        print('Spread helps')
if(float(ethereumMM1) + float(ethereumMM2) < 0.3):
    print('not enough ethereum calling price')
    need = 0.31 - (float(ethereumMM1) + float(ethereumMM2))
    ticker = clientPrice.get_ticker('GMB-ETH')
    amount = str(int(need / float(float(ticker['price']))))
    if(int(amount) < 1000):
        amount = '1000'
    if(float(ethereumMM1) < float(ethereumMM2)):
        order = clientMM1.create_limit_order('GMB-ETH', Client.SIDE_SELL, ticker['price'], amount) #place to sell
        clientPrice.create_market_order('GMB-ETH', Client.SIDE_BUY, client_oid = order['orderId'], size=int(amount)) #buying it
        print('Price helps')
    else:
        order = clientMM2.create_limit_order('GMB-ETH', Client.SIDE_SELL, ticker['price'], amount) #place to sell
        clientPrice.create_market_order('GMB-ETH', Client.SIDE_BUY, client_oid = order['orderId'], size=int(amount)) #buying it
        print('Price helps')
if(float(bitcoinMM1) + float(bitcoinMM2) < 0.03):
    print('not enough bitcoin calling price')
    need = 0.033 - (float(bitcoinMM1) + float(bitcoinMM2))
    ticker = clientPrice.get_ticker('GMB-BTC')
    amount = str(int(need / float(float(ticker['price']))))
    if(int(amount) < 1000):
        amount = '1000'
    if(float(bitcoinMM1) < float(bitcoinMM2)):
        order = clientMM1.create_limit_order('GMB-BTC', Client.SIDE_SELL, str(ticker['price']), amount) #place to sell
        clientPrice.create_market_order('GMB-BTC', Client.SIDE_BUY, client_oid = order['orderId'], size=int(amount)) #buying it
        print('Price helps')
    else:
        order = clientMM2.create_limit_order('GMB-BTC', Client.SIDE_SELL, str(ticker['price']), amount) #place to sell
        clientPrice.create_market_order('GMB-BTC', Client.SIDE_BUY, client_oid = order['orderId'], size=int(amount)) #buying it
        print('Price helps')
#refill
def refill():
    if(tetherMM1 > tetherMM2):
        golden = (float(tetherMM1) + float(tetherMM2))/2
        refill = float(tetherMM1) - golden
        ticker = clientMM1.get_ticker('GMB-USDT')
        amount = str(int(refill / float(ticker['price'])))
        if(int(amount) < 1000):
            amount = '1000'
        order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_SELL, str(ticker['price']), amount) #place to sell
        clientMM1.create_market_order('GMB-USDT', Client.SIDE_BUY, client_oid = order['orderId'], size=int(amount)) #buying it
        print('Rebalancing USDT')
def getrange():
    d = datetime.utcnow()
    unixtime = calendar.timegm(d.utctimetuple())
    print(unixtime)
    clientMM1 = Client('', '', '')
    klines = clientMM1.get_kline_data('', '5min', unixtime-600, unixtime-300)
    if(str(klines) != '[]'):
        print(str(klines) + ' :USDT')
        candles = klines[0]
        return candles[1], candles[2]
    else:
        return None

def trading():
    global up1
    if(getrange() == None):
        #USDT
        ticker1 = clientMM1.get_ticker('GMB-USDT')
        topask = ticker1['bestAsk']
        topbid = ticker1['bestBid']
        delta = rand.uniform(0.000001,0.000007)
        if(up1 == True and float(ticker1['price']) < float(topask)-delta):
            print('go up:USDT')
            ticker1 = clientMM1.get_ticker('GMB-USDT')
            minsell = float(ticker1['price'])+delta
            minask = str(minsell)
            print('minasks USDT: ' + minasks)
            size = rand.uniform(1050.1, 1170.1)
            sizes = str(size)
            amounts = sizes[0]+sizes[1]+sizes[2]+sizes[3]+sizes[4]+sizes[5]+sizes[6]
            if(float(tetherMM1) < float(tetherMM2)):
                order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts) #place to buy
                     #selling it
                clientMM2.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts,client_oid = order['orderId'])
                print('MM1 sells to MM2:USDT')
            else:
                order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts) #place to buy
                     #selling it
                clientMM1.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts,client_oid = order['orderId'])
                print('MM2 sells to MM1:USDT')
        else:
            up1 = False
        if(up1 == False and float(ticker1['price']) > float(topbid)+delta):
            print('go down:USDT')
            ticker1 = clientMM1.get_ticker('GMB-USDT')
            maxbuy = float(ticker1['price'])-delta
            minask = str(maxbuy)
            if(len(minask) == 7):
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]
            else:
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]
            print('minasks USDT: ' + minasks)
            size = rand.uniform(1250.1, 1370.1)
            sizes = str(size)
            amounts = sizes[0]+sizes[1]+sizes[2]+sizes[3]+sizes[4]+sizes[5]+sizes[6]
            if(float(tetherMM1) < float(tetherMM2)):
                order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts) #place to buy
                     #selling it
                clientMM1.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts,client_oid = order['orderId'])
                print('MM1 sells to MM2:USDT')
            else:
                order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts) #place to buy
                     #selling it
                clientMM2.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts,client_oid = order['orderId'])
                print('MM2 sells to MM1:USDT')
        else:
            up1 = True
    else:
        #USDT
        openedcandle, closedcandle = getrange()
        ticker1 = clientMM1.get_ticker('GMB-USDT')
        topask = ticker1['bestAsk']
        topbid = ticker1['bestBid']
        if(up1 == True and float(closedcandle) < float(topask)-0.000001):
            print('go up:USDT')
            delta = 0.000001
            ticker1 = clientMM1.get_ticker('GMB-USDT')
            minsell = float(ticker1['price'])+delta
            minask = str(minsell)
            if(len(minask) == 7):
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]
            else:
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]
            print('minasks USDT: ' + minasks)
            size = rand.uniform(1050.1, 1170.1)
            sizes = str(size)
            amounts = sizes[0]+sizes[1]+sizes[2]+sizes[3]+sizes[4]+sizes[5]+sizes[6]
            if(float(tetherMM1) < float(tetherMM2)):
                order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts) #place to buy
                     #selling it
                clientMM2.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts,client_oid = order['orderId'])
                print('MM1 sells to MM2:USDT')
            else:
                order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts) #place to buy
                     #selling it
                clientMM1.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts,client_oid = order['orderId'])
                print('MM2 sells to MM1:USDT')
        else:
            up1 = False
        if(up1 == False and float(closedcandle) > float(topbid)+delta):
            print('go down:USDT')
            delta = 0.000001
            ticker1 = clientMM1.get_ticker('GMB-USDT')
            maxbuy = float(ticker1['price'])-delta
            minask = str(maxbuy)
            if(len(minask) == 7):
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]
            else:
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]
            print('minasks USDT: ' + minasks)
            size = rand.uniform(1250.1, 1370.1)
            sizes = str(size)
            amounts = sizes[0]+sizes[1]+sizes[2]+sizes[3]+sizes[4]+sizes[5]+sizes[6]
            if(float(tetherMM1) < float(tetherMM2)):
                order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts) #place to buy
                     #selling it
                clientMM1.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts,client_oid = order['orderId'])
                print('MM1 sells to MM2:USDT')
            else:
                order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, amounts) #place to buy
                     #selling it
                clientMM2.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, amounts,client_oid = order['orderId'])
                print('MM2 sells to MM1:USDT')
        else:
            up1 = True
    getrange()
    if(getrange() != None):
        #tradin
        openedcandle, closedcandle = getrange()
        minsell = closedcandle
        print('minsell: ' +minsell)
        #getting currentspread
        ticker1 = clientMM1.get_ticker('GMB-USDT')
        ticker2 = client.get_ticker('BTC-USDT')
        topask = ticker1['bestAsk']
        topbid = ticker1['bestBid']
        if(float(openedcandle) >= float(closedcandle)):
            delta = rand.uniform(0.000001,float(closedcandle)-float(topbid))
            minask = str(float(minsell) + delta)
            minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7] #increment avoid
            if(float(tetherMM1) < float(tetherMM2)):
                order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, '500') #place to buy
                 #selling it
                clientMM1.create_market_order('GMB-USDT', Client.SIDE_SELL, client_oid = order['orderId'], size=500)
                
                print('MM2 sells to MM1: USDT')
            else:
                order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-USDT', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: USDT')
            if(float(bitcoinMM1) < float(bitcoinMM2)):
                #get spread for GMB/BTC
                minsell_btc = str(float(minsell) / float(ticker2['price']))
                delta_btc = delta / float(ticker2['price'])
                minask = str(float(minsell_btc) - delta_btc)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-BTC', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-BTC', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM2 sells to MM1: BTC')
            else:
                #get spread for GMB/BTC
                minsell_btc = str(float(minsell) / float(ticker2['price']))
                delta_btc = delta / float(ticker2['price'])
                minask = str(float(minsell_btc) - delta_btc)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-BTC', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-BTC', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: BTC')
            if(float(ethereumMM1) < float(ethereumMM2)):
                #get spread for GMB/ETH
                ticker3 = client.get_ticker('ETH-USDT')
                minsell_eth = str(float(minsell) / float(ticker3['price']))
                delta_eth = delta / float(ticker3['price'])
                minask = str(float(minsell_eth) - delta_eth)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-ETH', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-ETH', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM2 sells to MM1: ETH')
            else:
                #get spread for GMB/ETH
                ticker3 = client.get_ticker('ETH-USDT')
                minsell_eth = str(float(minsell) / float(ticker3['price']))
                delta_eth = delta / float(ticker3['price'])
                minask = str(float(minsell_eth) - delta_eth)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-ETH', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-ETH', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: ETH')
            minask = str(float(minsell) + delta)
            minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7] #increment avoid
            if(float(tetherMM1) < float(tetherMM2)):
                order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, '500') #place to buy
                 #selling it
                clientMM1.create_market_order('GMB-USDT', Client.SIDE_SELL, client_oid = order['orderId'], size=500)
                
                print('MM2 sells to MM1: USDT')
            else:
                order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-USDT', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: USDT')
            if(float(bitcoinMM1) < float(bitcoinMM2)):
                #get spread for GMB/BTC
                minsell_btc = str(float(minsell) / float(ticker2['price']))
                delta_btc = delta / float(ticker2['price'])
                minask = str(float(minsell_btc) - delta_btc)
                order = clientMM1.create_limit_order('GMB-BTC', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-BTC', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM2 sells to MM1: BTC')
            else:
                #get spread for GMB/BTC
                minsell_btc = str(float(minsell) / float(ticker2['price']))
                delta_btc = delta / float(ticker2['price'])
                minask = str(float(minsell_btc) - delta_btc)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-BTC', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-BTC', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: BTC')
            if(float(ethereumMM1) < float(ethereumMM2)):
                #get spread for GMB/ETH
                ticker3 = client.get_ticker('ETH-USDT')
                minsell_eth = str(float(minsell) / float(ticker3['price']))
                delta_eth = delta / float(ticker3['price'])
                minask = str(float(minsell_eth) - delta_eth)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-ETH', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-ETH', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM2 sells to MM1: ETH')
            else:
                #get spread for GMB/ETH
                ticker3 = client.get_ticker('ETH-USDT')
                minsell_eth = str(float(minsell) / float(ticker3['price']))
                delta_eth = delta / float(ticker3['price'])
                minask = str(float(minsell_eth) - delta_eth)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-ETH', Client.SIDE_BUY, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-ETH', Client.SIDE_SELL, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: ETH')
        else:
            delta = rand.uniform(0.000001,float(topask)-float(closedcandle))
            minask = str(float(minsell) - delta)
            minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7] #increment avoid
            if(float(tetherMM1) < float(tetherMM2)):
                order = clientMM1.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, '500') #place to buy
                 #selling it
                clientMM2.create_market_order('GMB-USDT', Client.SIDE_BUY, client_oid = order['orderId'], size=500)
                
                print('MM2 sells to MM1: USDT')
            else:
                order = clientMM2.create_limit_order('GMB-USDT', Client.SIDE_SELL, minasks, '500') #place to buy
                clientMM1.create_market_order('GMB-USDT', Client.SIDE_BUY, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: USDT')
            if(float(bitcoinMM1) < float(bitcoinMM2)):
                #get spread for GMB/BTC
                minsell_btc = str(float(minsell) / float(ticker2['price']))
                delta_btc = delta / float(ticker2['price'])
                minask = str(float(minsell_btc) - delta_btc)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-BTC', Client.SIDE_SELL, minasks, '500') #place to buy
                clientMM2.create_market_order('GMB-BTC', Client.SIDE_BUY, client_oid = order['orderId'], size=500) #selling it
                print('MM2 sells to MM1: BTC')
            else:
                #get spread for GMB/BTC
                minsell_btc = str(float(minsell) / float(ticker2['price']))
                delta_btc = delta / float(ticker2['price'])
                minask = str(float(minsell_btc) - delta_btc)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM2.create_limit_order('GMB-BTC', Client.SIDE_SELL, minasks, '500') #place to buy
                clientMM1.create_market_order('GMB-BTC', Client.SIDE_BUY, client_oid = order['orderId'], size=500) #selling it
                print('MM1 sells to MM2: BTC')
            if(float(ethereumMM1) < float(ethereumMM2)):
                #get spread for GMB/ETH
                ticker3 = client.get_ticker('ETH-USDT')
                minsell_eth = str(float(minsell) / float(ticker3['price']))
                delta_eth = delta / float(ticker3['price'])
                minask = str(float(minsell_eth) - delta_eth)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM1.create_limit_order('GMB-ETH', Client.SIDE_SELL, minasks, '500') #place to sell
                clientMM2.create_market_order('GMB-ETH', Client.SIDE_BUY, client_oid = order['orderId'], size=500) #buying it
                print('MM2 sells to MM1: ETH')
            else:
                #get spread for GMB/ETH
                ticker3 = client.get_ticker('ETH-USDT')
                minsell_eth = str(float(minsell) / float(ticker3['price']))
                delta_eth = delta / float(ticker3['price'])
                minask = str(float(minsell_eth) - delta_eth)
                minasks = minask[0]+minask[1]+minask[2]+minask[3]+minask[4]+minask[5]+minask[6]+minask[7]+minask[8]+minask[9]+minask[10]+minask[11] #increment avoid
                order = clientMM2.create_limit_order('GMB-ETH', Client.SIDE_SELL, minasks, '500') #place to sell
                clientMM1.create_market_order('GMB-ETH', Client.SIDE_BUY, client_oid = order['orderId'], size=500) #buying it
                print('MM1 sells to MM2: ETH')

def getbalances():
    clientMM1 = Client('', '', '')
    clientMM2 = Client('', '', '')
    clientPrice = Client('', '', '')
    clientSpread = Client('', '', '')
    clientMM1.cancel_all_orders()
    clientMM2.cancel_all_orders()
    clientPrice.cancel_all_orders()
    ticker = clientMM1.get_ticker('GMB-USDT')
    ticker1 = clientMM1.get_ticker('BTC-USDT')
    ticker2 = clientMM1.get_ticker('ETH-USDT')
    account1 = clientMM1.get_account('6107ef85116de4000646da9a')
    account2 = clientMM1.get_account('5c6a4a9599a1d81939341bec')
    account3 = clientMM1.get_account('5c6a507f99a1d8174318f7fe')
    account4 =  clientMM1.get_account('5e4acb63e0d68100089dc874')
    bitcoinMM1 = account4['available']
    ethereumMM1 = account3['available']
    tetherMM1 = account1['available']
    gambMM1 = account2['available']
    print('Balances MM1:')
    print(tetherMM1 + ' USDT')
    print(gambMM1 + ' GMB')
    print(ethereumMM1 + ' ETH')
    print(bitcoinMM1 + ' BTC')
    print('In Total($): ' + str(float(ticker['price'])*float(gambMM1)+float(tetherMM1)+float(ethereumMM1)*float(ticker2['price'])+float(bitcoinMM1)*float(ticker1['price']))) #MM1

    ticker = clientMM2.get_ticker('GMB-USDT')
    ticker1 = clientMM2.get_ticker('BTC-USDT')
    ticker2 = clientMM2.get_ticker('ETH-USDT')
    account1 = clientMM2.get_account('6107ee080a84dc00066e13dc')
    account2 = clientMM2.get_account('5c6a4b0199a1d81b25aa9362')
    account3 = clientMM2.get_account('5c88d6480d48eb05aef3edf2')
    account4 =  clientMM2.get_account('5c6a4f9699a1d81b25d38097')
    bitcoinMM2 = account4['available']
    ethereumMM2 = account3['available']
    tetherMM2 = account1['available']
    gambMM2 = account2['available']
    print('Balances MM2:')
    print(tetherMM2 + ' USDT')
    print(gambMM2 + ' GMB')
    print(ethereumMM2 + ' ETH')
    print(bitcoinMM2 + ' BTC')
    print('In Total($): ' + str(float(ticker['price'])*float(gambMM2)+float(tetherMM2)+float(ethereumMM2)*float(ticker2['price'])+float(bitcoinMM2)*float(ticker1['price']))) #MM2
    ticker = clientPrice.get_ticker('GMB-USDT')
    ticker1 = clientPrice.get_ticker('BTC-USDT')
    ticker2 = clientPrice.get_ticker('ETH-USDT')
    account1 = clientPrice.get_account('')
    account2 = clientPrice.get_account('')
    account3 = clientPrice.get_account('')
    account4 =  clientPrice.get_account('')
    bitcoinPrice = account4['available']
    ethereumPrice = account3['available']
    tetherPrice = account1['available']
    gambPrice = account2['available']
    print('Balances Price:')
    print(tetherPrice + ' USDT')
    print(gambPrice + ' GMB')
    print(ethereumPrice + ' ETH')
    print(bitcoinPrice + ' BTC')
    print('In Total($): ' + str(float(ticker['price'])*float(gambPrice)+float(tetherPrice)+float(ethereumPrice)*float(ticker2['price'])+float(bitcoinPrice)*float(ticker1['price']))) #Price
    ticker = clientSpread.get_ticker('GMB-USDT')
    ticker1 = clientSpread.get_ticker('BTC-USDT')
    ticker2 = clientSpread.get_ticker('ETH-USDT')
    account1 = clientSpread.get_account('')
    account2 = clientSpread.get_account('')
    account3 = clientSpread.get_account('')
    account4 =  clientSpread.get_account('')
    
    bitcoinSpread = account4['available']
    ethereumSpread = account3['available']
    tetherSpread = account1['available']
    gambSpread = account2['available']
    print('Balances Spread:')
    print(tetherSpread + ' USDT')
    print(gambSpread + ' GMB')
    print(ethereumSpread + ' ETH')
    print(bitcoinSpread + ' BTC')
    print('In Total($): ' + str(float(ticker['price'])*float(gambSpread)+float(tetherSpread)+float(ethereumSpread)*float(ticker2['price'])+float(bitcoinSpread)*float(ticker1['price']))) #Spread
    ticker = client.get_ticker('GMB-USDT')
    ticker1 = client.get_ticker('BTC-USDT')
    ticker2 = client.get_ticker('ETH-USDT')
    account1 = client.get_account('')
    account2 = client.get_account('')
    account3 = client.get_account('')
    account4 =  client.get_account('')
        
    bitcoinSpread = account4['available']
    ethereumSpread = account3['available']
    tetherSpread = account1['available']
    gambSpread = account2['available']
    print('Balances Sales:')
    print(tetherSpread + ' USDT')
    print(gambSpread + ' GMB')
    print(ethereumSpread + ' ETH')
    print(bitcoinSpread + ' BTC')
    print('In Total($): ' + str(float(ticker['price'])*float(gambSpread)+float(tetherSpread)+float(ethereumSpread)*float(ticker2['price'])+float(bitcoinSpread)*float(ticker1['price']))) #Sales
    clientMM1.cancel_all_orders()
    clientMM2.cancel_all_orders()
    clientSpread.cancel_all_orders()
    clientPrice.cancel_all_orders()
schedule.every(20).seconds.do(trading)
schedule.every(15).seconds.do(getbalances)
schedule.every(15).seconds.do(getrange)
schedule.every(10).seconds.do(refill)
while(1):
    schedule.run_pending()
    time.sleep(30)

