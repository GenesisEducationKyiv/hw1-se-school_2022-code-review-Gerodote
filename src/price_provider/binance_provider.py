from .general_part import AbstractPriceProvider, symbol_t, AbstractPriceStorage
from .websockets.binance_websockets.binance_websocket_starter import BinanceWebsocketStarter
from .websockets.binance_websockets.binance_data_parser import BinanceBooktickerCreatorStreams, BinanceWebsocketBooktickerAveragePrice
from .websockets.binance_websockets.binance_stream_receiver import BinanceWebsocketStreamsReceiver
from .websockets.how_to_use_it import start_websockets
from .price_storage import PriceStorage
from .cache_impl import CacheToListInMemoryAutoDelete


class BinancePriceProvider(AbstractPriceProvider):
    def __init__(self, symbol:symbol_t) -> None: 
        # because there's still no support in our out API for multiple subscription data.
        self.__price_storage:AbstractPriceStorage = PriceStorage(CacheToListInMemoryAutoDelete(300))
        # if was support for multiple streams, here would be ...(...(...), "stream","data").
        message_receiver = BinanceWebsocketStreamsReceiver(BinanceWebsocketBooktickerAveragePrice(self.__price_storage), None, None)            
        start_websockets([symbol], BinanceBooktickerCreatorStreams(),BinanceWebsocketStarter(), message_receiver)
            
    def get_price(self, symbol: symbol_t) -> float:
        return self.__price_storage.get_price(symbol)