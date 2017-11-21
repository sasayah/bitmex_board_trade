import bitmex_basic
import os

#bitmex = bitmex_basic.BitMEX(symbol='XBTUSD', apiKey=os.environ["API_TEST_KEY"], apiSecret=os.environ["API_TEST_SECRET"], base_uri='https://testnet.bitmex.com/api/v1/')
#print(bitmex.market_depth())

def number_of_series(coinpair,mini_size,base_uri):
    bitmex = bitmex_basic.BitMEX(symbol=coinpair, apiKey=os.environ["API_TEST_KEY"], apiSecret=os.environ["API_TEST_SECRET"], base_uri=base_uri)
    buy_count = 0
    sell_count = 0
    market_boards = bitmex.market_depth()
   #print(market_boards)
    for board in market_boards:
        if board['bidSize'] < mini_size:
            buy_count+=1
        else: break
    for board in market_boards:
        if board['askSize'] < mini_size:
            sell_count+=1
        else: break
    return {'buy':buy_count, 'sell':sell_count}

#print(number_of_series('XBTUSD',28000,'https://testnet.bitmex.com/api/v1/'))



