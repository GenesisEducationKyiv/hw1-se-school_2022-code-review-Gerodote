from time import sleep
from typing import Dict, List, Union
import logging
import json

from binance.spot import Spot as Client
from binance.lib.utils import config_logging

from src.price_provider.general_part import symbol_t, AbstractPriceStorage
from src.price_provider.websockets.general_part import AbstractMessageDataProcessing, stream_t, AbstractCreatorStreamsStrings
from src.price_provider.websockets.binance_websockets.binance_websocket_starter import BinanceWebsocketStarter
from src.price_provider.websockets.binance_websockets.binance_data_parser import BinanceWebsocketBooktickerCreatorStreams, BinanceWebsocketBooktickerAveragePrice
from src.price_provider.websockets.binance_websockets.binance_stream_receiver import BinanceWebsocketStreamsReceiver
from src.price_provider.price_storage import PriceStorage

config_logging(logging, logging.DEBUG, log_file='binance_logs.txt')


class basic_callback:

    def __init__(self) -> None:
        self.message: Dict = {}

    def __call__(self, message):
        with open('file.txt', 'w') as file:
            file.write(json.dumps(message, indent=4))
        self.message = message


def test_subscribe_one_stream():
    with BinanceWebsocketStarter() as sth:
        sth2 = basic_callback()
        sth.subscribe_one_stream(stream_t(name='btcusdt@bookTicker'), sth2)
        '''
        We should get sth like this:
            {
            "u":400900217,     // order book updateId
            "s":"BNBUSDT",     // symbol
            "b":"25.35190000", // best bid price
            "B":"31.21000000", // best bid qty
            "a":"25.36520000", // best ask price
            "A":"40.66000000"  // best ask qty
            }
        '''
        sleep(25)
        result = False
        if 'u' in sth2.message.keys():
            result = True
        assert (result)


class DumbDataProcessor(AbstractMessageDataProcessing):

    def __init__(self):
        self._inner_data = None

    def __call__(self, data: Union[Dict, List]) -> None:
        self._inner_data = data

    def get_inner_data(self):
        return self._inner_data


def test_binance_stream_receiver():
    sth_1 = DumbDataProcessor()
    sth = BinanceWebsocketStreamsReceiver(sth_1, None, None)
    sth('{"text":"txt"}')
    assert sth_1.get_inner_data() == {"text": "txt"}


def test_REST_bookTicker_is_same_as_ws_book_ticker():
    ''' test is passed, though problem: TwistedIsNotRestartable. 
    Just try run this test by itself without others. 
    for example : pytest -k REST 
    This command will run only tests with this substring.
   '''
    symbols_strings = ["BTCUAH", "BTCUSDT"]

    symbols_lst: List[symbol_t] = [
        symbol_t(name=symbol) for symbol in symbols_strings
    ]
    stream_creator: AbstractCreatorStreamsStrings = BinanceWebsocketBooktickerCreatorStreams(
    )
    streams: List[stream_t] = stream_creator(symbols=symbols_lst)
    price_storage: AbstractPriceStorage = PriceStorage()
    data_processor: AbstractMessageDataProcessing = BinanceWebsocketBooktickerAveragePrice(
        price_storage)

    with BinanceWebsocketStarter() as binance_websocket_starter:
        if len(streams) == 1:
            binance_websocket_starter.subscribe_one_stream(
                streams[0],
                BinanceWebsocketStreamsReceiver(data_processor, None, None))
        else:
            binance_websocket_starter.subscribe_multiple_streams(
                streams,
                BinanceWebsocketStreamsReceiver(data_processor, "stream",
                                                "data"))

        spot_client = Client()

        for_do_while: bool = True
        count_how_many_times_checked = 0
        while (for_do_while):
            sleep(15)
            for symbol in symbols_lst:
                try:
                    data_processor.price_storage.get_price(symbol=symbol)
                except KeyError:
                    count_how_many_times_checked += 1
                    break
            if count_how_many_times_checked > 4:
                for_do_while = False

        from_REST_API = spot_client.book_ticker(
            symbols=[symbol.name for symbol in symbols_lst])
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
        average_from_REST_API = [
            (float(sth['bidPrice']) + float(sth['askPrice'])) / 2
            for sth in from_REST_API
        ]
        assert (len([(
            average_from_REST_API[i] == data_processor.price_storage.get_price(
                symbol=symbols_lst[i]))
                     for i in range(len(symbols_lst))]) == len(symbols_lst))
