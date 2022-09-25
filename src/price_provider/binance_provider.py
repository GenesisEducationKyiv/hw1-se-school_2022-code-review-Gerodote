from .cache_impl import CacheToListInMemoryAutoDelete
from .general_part import AbstractPriceProvider, AbstractPriceStorage, symbol_t
from .price_storage import PriceStorage
from .websockets.binance_websockets.binance_data_parser import (
    BinanceWebsocketBooktickerAveragePrice,
    BinanceWebsocketBooktickerCreatorStreams)
from .websockets.binance_websockets.binance_stream_receiver import \
    BinanceWebsocketStreamsReceiver
from .websockets.binance_websockets.binance_websocket_starter import \
    BinanceWebsocketStarter
from .websockets.how_to_use_it import start_websockets


class BinanceWebsocketPriceProvider(AbstractPriceProvider):

    def __init__(self, symbol: symbol_t) -> None:
        # because there's still no support in our out API for multiple subscription data.
        price_storage: AbstractPriceStorage = PriceStorage(
            CacheToListInMemoryAutoDelete(300))
        # if was support for multiple streams, here would be ...(...(...), "stream","data").
        self.__data_processor = BinanceWebsocketBooktickerAveragePrice(
            price_storage)
        message_receiver = BinanceWebsocketStreamsReceiver(
            self.__data_processor, None, None)
        start_websockets([symbol], BinanceWebsocketBooktickerCreatorStreams(),
                         BinanceWebsocketStarter(), message_receiver)

    def get_price(self, symbol: symbol_t) -> float:
        return self.__data_processor.price_storage.get_price(symbol)
