from ctypes import wstring_at
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from ..price_provider.getter_price_binance import BookTickerPriceBinance
from time import sleep

def test_REST_bookTicker_is_same_as_ws_book_ticker():
    spot_client = Client()
    symbol = 'BTCUAH'
    ws_client = BookTickerPriceBinance(symbol=symbol) 
    for_do_while:bool = True
    count_how_many_times_checked = 0
    while(for_do_while):
        sleep(15)
        if ws_client.get_price(symbol=symbol) is not None:
            for_do_while = False
        if count_how_many_times_checked > 8:
            for_do_while = False
    from_REST_API = spot_client.book_ticker(symbol=symbol)
    '''
        here we got sth like this:
            {
            "symbol": "LTCBTC",
            "bidPrice": "0.00378600",
            "bidQty": "3.50000000",
            "askPrice": "0.00379100",
            "askQty": "26.69000000"
            }
    '''
    average_from_REST_API = (float(from_REST_API['bidPrice']) + float(from_REST_API['askPrice'] ))/ 2
    assert(average_from_REST_API == ws_client.get_price(symbol=symbol))
    ws_client.stop_ws()
       
    
