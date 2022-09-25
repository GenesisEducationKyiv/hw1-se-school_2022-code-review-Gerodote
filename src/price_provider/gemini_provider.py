from time import sleep
from typing import List

from .cache_impl import CacheToFileNoDelete
from .general_part import AbstractPriceProvider, symbol_t
from .price_storage import PriceStorage
from .websockets.gemini_websockets.gemini_data_parser import (
    GeminiTopOfBookCreatorStream, GeminiTopOfBookDataProcessing)
from .websockets.gemini_websockets.gemini_websocket_starter import \
    GeminiWebsocketStarter
from .websockets.general_part import (AbstractCreatorStreamsStrings,
                                      AbstractWebsocketStarter, stream_t)
from .websockets.streams_receiver import GeneralWebsocketStreamsReceiver


class GeminiPriceProvider(AbstractPriceProvider):

    def __init__(self, symbol: symbol_t):
        symbols_lst: List[symbol_t] = [symbol]
        stream_creator: AbstractCreatorStreamsStrings = \
            GeminiTopOfBookCreatorStream()
        stream: stream_t = stream_creator(symbols=symbols_lst)
        self.__data_processor: GeminiTopOfBookDataProcessing = \
            GeminiTopOfBookDataProcessing(
            PriceStorage(CacheToFileNoDelete("cache_prices_gemini.txt")))
        ws_starter: AbstractWebsocketStarter = GeminiWebsocketStarter()

        ws_starter.subscribe_one_stream(
            stream,
            message_handler=GeneralWebsocketStreamsReceiver(
                self.__data_processor, None, None))
        sleep(15)

    def get_price(self, symbol: symbol_t) -> float:
        return self.__data_processor.price_storage.get_price(symbol)
