from time import sleep
from typing import List

from .cache_impl import CacheToFileNoDelete
from .general_part import AbstractPriceProvider, symbol_t
from .price_storage import PriceStorage
from .websockets.gemini_websockets.gemini_data_parser import (
    GeminiWebsocketTopOfBookCreatorStream,
    GeminiWebsocketTopOfBookDataProcessing)
from .websockets.gemini_websockets.gemini_websocket_starter import \
    GeminiWebsocketStarter
from .websockets.general_part import (AbstractCreatorStreamsStrings,
                                      AbstractWebsocketStarter, stream_t)
from .websockets.how_to_use_it import start_websockets
from .websockets.streams_receiver import GeneralWebsocketStreamsReceiver


class GeminiWebsocketTopOfBookPriceProvider(AbstractPriceProvider):

    def __init__(self, symbol: symbol_t):
        symbols_lst: List[symbol_t] = [symbol]
        self.__data_processor: GeminiWebsocketTopOfBookDataProcessing = \
            GeminiWebsocketTopOfBookDataProcessing(
            PriceStorage(CacheToFileNoDelete("cache_prices_gemini.txt")))
        start_websockets(
            symbols=symbols_lst,
            streams_name_creator=GeminiWebsocketTopOfBookCreatorStream(),
            websocket_net_handler=GeminiWebsocketStarter(),
            websocket_message_receiver=GeneralWebsocketStreamsReceiver(
                self.__data_processor, None, None))

    def get_price(self, symbol: symbol_t) -> float:
        return self.__data_processor.price_storage.get_price(symbol)
