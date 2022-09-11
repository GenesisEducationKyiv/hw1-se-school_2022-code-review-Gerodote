from time import sleep
from typing import List

from binance.spot import Spot as Client

from ..src.price_provider.websockets.general_part import symbol_t, stream_t, AbstractCreaterStreamsStrings, AbstractPriceGetterSetter
from ..src.price_provider.websockets.binance_websockets.binance_websocket_starter import BinanceWebsocketStarter
from ..src.price_provider.websockets.binance_websockets.binance_data_parser import BinanceBooktickerCreaterStreams, BinanceWebsocketBooktickerAveragePrice
from ..src.price_provider.websockets.streams_receiver import WebsocketStreamsReceiver
from ..src.price_provider.websockets.price_storage import PriceStorage

def test_REST_bookTicker_is_same_as_ws_book_ticker():
    symbols_strings = ["BTCUAH", "BTCUSDT"]
    
    symbols: List[symbol_t] = [symbol_t(name=symbol) for symbol in symbols_strings]
    StreamCreator: AbstractCreaterStreamsStrings = BinanceBooktickerCreaterStreams(
    )
    streams: List[stream_t] = StreamCreator(symbols=symbols)
    price_storage:AbstractPriceGetterSetter = PriceStorage()

    binance_websocket_starter = BinanceWebsocketStarter()
    if len(streams) == 1:
        binance_websocket_starter.subscribe_one_stream(streams[0], WebsocketStreamsReceiver(BinanceWebsocketBooktickerAveragePrice,None,price_storage))
    else:
        binance_websocket_starter.subscribe_multiple_streams(streams, WebsocketStreamsReceiver(BinanceWebsocketBooktickerAveragePrice,"stream",price_storage))
    
    
    spot_client = Client()
    
    for_do_while:bool = True
    count_how_many_times_checked = 0
    while(for_do_while):
        sleep(15)
        for symbol in symbols:
            if price_storage.price(symbol=symbol) is not None:
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
    assert(len([average_from_REST_API == price_storage.price(symbol=symbol)]) == len(symbols))

       
    
if __name__ == '__main__':
    test_REST_bookTicker_is_same_as_ws_book_ticker()