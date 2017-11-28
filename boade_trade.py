import bitmex_basic
import os
import sys
from time import sleep

#bitmex = bitmex_basic.BitMEX(symbol='XBTUSD', apiKey=os.environ["API_TEST_KEY"], apiSecret=os.environ["API_TEST_SECRET"], base_uri='https://testnet.bitmex.com/api/v1/')
#print(bitmex.market_depth())

class board_trade():

    def __init__(self,base_uri, symbol):
        self.bitmex = bitmex_basic.BitMEX(symbol=symbol, apiKey=os.environ["API_TEST_KEY"], apiSecret=os.environ["API_TEST_SECRET"], base_uri=base_uri)
        self.market_boards = self.bitmex.market_depth()


    def number_of_series(self,mini_size):
        buy_count = 0
        sell_count = 0
    #print(market_boards)
        for board in self.market_boards:
            if board['bidSize'] < mini_size:
                buy_count+=1
            else: break
        for board in self.market_boards:
            if board['askSize'] < mini_size:
                sell_count+=1
            else: break
        return {'buy':buy_count, 'sell':sell_count}

    #print(number_of_series('XBTUSD',28000,'https://testnet.bitmex.com/api/v1/'))

    def decide_buy_sell(self,series_num,decide_big,decide_samll):
        if(decide_big<decide_samll):
            print('最小値と最大値が間違っています')
            sys.exit(1)

        if(series_num['buy']>=decide_big and series_num['sell']<decide_samll):
            return 'sell'
        elif(series_num['sell']>=decide_big and series_num['buy']<decide_samll):
            return 'buy'
        else:
            return 'wait'


    def decide_price(self,buy_or_sell):
        price = 0.0
        if(buy_or_sell=='buy'):
            price = self.market_boards[0]['askPrice']
        elif(buy_or_sell=='sell'):
            price = self.market_boards[0]['bidPrice']
        return price
    
    def current_price(self):
        bid = self.market_boards[0]['bidPrice']
        ask = self.market_boards[0]['askPrice']
        return {'bid': bid,'ask': ask}


    #仕様は未定
    def decide_volume(self,buy_or_sell):
        volume = 0
        volume =  self.bitmex.wallet() * self.current_price()['bid']
        print(volume)
        return int(volume)


    def settle_price_func(self,buy_or_sell, series_num, price):
        reverse = 1
        if(buy_or_sell=='sell'):
            reverse = -1
            #怪しい
        reverse_buy_or_sell = ''
        if(buy_or_sell=='buy'):
            reverse_buy_or_sell = 'sell'
        elif(buy_or_sell=='sell'):
            reverse_buy_or_sell = 'buy'
        print(series_num)

        settle_price = price + 0.5*series_num[reverse_buy_or_sell]*reverse
        return settle_price

    
    def lost_cut_price_func(self,buy_or_sell, price):
        reverse = 1
        if(buy_or_sell=='buy'):
            reverse = -1
            #怪しい
        lost_cut_price = price + 0.5*reverse
        return lost_cut_price
        



    
    def trade(self,mini_size,decide_big,decide_samll):
        series_num = self.number_of_series(mini_size)
        print(series_num)
        buy_or_sell = self.decide_buy_sell(series_num,decide_big,decide_samll)
        print(buy_or_sell)
        if(buy_or_sell == 'wait'):
            return 'wait'
        else:
            price = self.decide_price(buy_or_sell)
            volume = self.decide_volume(buy_or_sell)
            order_ID = ''
            change_price = 0.0
            count = 0
            count2 = 0
            settle_price = self.settle_price_func(buy_or_sell, series_num, price)
            lost_cut_price = self.lost_cut_price_func(buy_or_sell, price)
            if(buy_or_sell=='buy'):
                order_ID = self.bitmex.buy(volume, price)['orderID']
                change_price -= 0.5
            elif(buy_or_sell=='sell'):
                order_ID = self.bitmex.sell(volume, price)['orderID']
                change_price += 0.5

            while(self.bitmex.position() == [] and count < 10):
                if(buy_or_sell=='buy' and self.decide_price(buy_or_sell) - price <= change_price):
                    break
                elif(buy_or_sell=='sell' and self.decide_price(buy_or_sell) - price >= change_price):
                    break
                sleep(1)
                count += 1
            print('order_ID: ' + order_ID)

            self.bitmex.cancel(order_ID)
            position = self.bitmex.position()[0]['currentQty']
            if(position > 0):
                #利確設定
                if(buy_or_sell=='buy'):
                    self.bitmex.sell(position,settle_price)
                elif(buy_or_sell=='sell'):
                    self.bitmex.buy(position,settle_price)

                #損切り設定
                while(self.bitmex.position() != [] and count2 < 10):
                    if(buy_or_sell=='buy' and self.current_price()['bid']<price):
                        break
                    elif(buy_or_sell=='sell' and self.current_price()['ask']>price):
                        break
                    sleep(1)
                    count += 1
                
                self.bitmex.closeAllPosition()


            

#while(True):
    board_trade1 = board_trade(symbol='XBTUSD', base_uri='https://testnet.bitmex.com/api/v1/')
    board_trade2 = board_trade(symbol='XBTUSD', base_uri='https://testnet.bitmex.com/api/v1/')
    board_trade1.trade(mini_size=1000,decide_big=3,decide_samll=2)
    bitmex = bitmex_basic.BitMEX(symbol='XBTUSD', apiKey=os.environ["API_TEST_KEY"], apiSecret=os.environ["API_TEST_SECRET"], base_uri='https://testnet.bitmex.com/api/v1/')
    bitmex.closeAllPosition()
    sleep(2)





            

            
                
                
                


        
            




    





