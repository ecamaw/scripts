#!/usr/bin/env python3

import json
import requests
from requests.auth import HTTPBasicAuth
import time

url='https://api.binance.com/api/'

# get requests
t1=time.clock()
servertime = requests.get(url+'v1/time')
prices_json = requests.get(url+'v1/ticker/allPrices')
prices_data = prices_json.json()
t2=time.clock()
print(t2-t1)
exit
neo_in = 10 # 10 NEO

coinsBTC = []
priceBTC = []
coinsETH = []
priceETH = []
coinsBNB = []
priceBNB = []
coinsAll = []
priceAll = []

# Get prices for all pairs
for i in range(0, len(prices_data),1):
    tmp = prices_data[i]    
    coinsAll.append(tmp['symbol'])
    priceAll.append(tmp['price'])
    if tmp['symbol'] == 'ETHBTC':
        eth_btc = float(tmp['price'])
        btc_eth = 1.0 /eth_btc
    elif tmp['symbol'] == 'BNBETH':
        bnb_eth = float(tmp['price'])
        eth_bnb = 1.0 / bnb_eth
    key, value = tmp['symbol'], tmp['price']
    if "BTC" in key:
        tmp = key.split("BTC",1)
        if tmp[0] == '':
            pass
        else:
            tmp.pop()
            tmp1 = tmp[0]
            coinsBTC.append(tmp1)
            priceBTC.append(value)
    elif "ETH" in key:
        tmp = key.split("ETH",1)
        if tmp[0] == '':
            pass
        else:
            tmp.pop(1)
            tmp1 = tmp[0]
            coinsETH.append(tmp1)
            priceETH.append(value)
    elif "BNB" in key:
        tmp = key.split("BNB",1)
        if tmp[0] == '':
            pass
        else:
            tmp.pop()
            tmp1 = tmp[0]
            coinsBNB.append(tmp1)
            priceBNB.append(value)

t1=time.clock()
# Calculate spreads: ETH-X-Y-ETH
crypto_in = 1
coins_out = {}
coinsX    = []
priceX    = []
coinsY    = []
priceY    = []

for i in range(0, len(coinsAll),1):
    if coinsAll[i] == "ETHUSDT":
        ethusdt = priceAll[i]

for i in range(0, len(coinsAll),1):
    if "ETH" in coinsAll[i]:
        tmp = coinsAll[i].split("ETH",1)
        if tmp[0] == '':
            pass
        elif tmp[0] == 'BNB':
            pass
        elif tmp[0] == 'VIB':
            pass
        else:
            tmp.pop()
            tmp1 = tmp[0]
            coinsX.append(tmp1)
            price_tmp = crypto_in * (1.0 / float(priceAll[i])) # ETH -> X
            priceX.append(price_tmp)
            
maxima = {}
for j in range(0, len(coinsX), 1):
    for k in range(0, len(coinsAll), 1):
        if coinsX[j] in coinsAll[k]:            
            if "ETH" in coinsAll[k]:
                pass
            else:
                tmp = coinsAll[k].split(coinsX[j],1)
                if tmp[0] == '':
                    tmp1=tmp[1]
                    coinsY.append(tmp1)
                    priceY.append(priceAll[k])
                elif tmp[1] == '':
                    tmp1=tmp[0]
                    coinsY.append(tmp1)
                    priceY.append(priceAll[k])
                else:
                    pass
                crypto_y = float(priceX[j]) * float(priceAll[k]) # X -> Y
                y1=tmp1+"ETH"
                y2="ETH"+tmp1
                for i in range(0, len(prices_data),1):
                    tmp = prices_data[i]    
                    if y1 in tmp['symbol']:
                        y_eth =  float(tmp['price'])                        
                    elif y2 in tmp['symbol']:
                        y_eth = 1.0 / float(tmp['price'])                        
                eth = crypto_y * y_eth                           # Y -> ETH
                method = "ETH"+"-"+str(coinsX[j])+"-"+tmp1+"-"+"ETH"
                maxima[method] = eth

maximum = maxima[max(maxima, key=maxima.get)]
crypto = {key for key, value in maxima.items() if value == maximum}
gain = maximum - crypto_in
t2=time.clock()
print(t2-t1)
print(crypto, str(gain*float(ethusdt)))
