from typing import List
from ...general_part import AbstractPriceStorage, symbol_t
from ..general_part import AbstractCreatorStreamsStrings, AbstractMessageDataProcessing, stream_t


class BinanceBooktickerCreatorStreams(AbstractCreatorStreamsStrings):
    '''
    According to https://docs.binance.us/?python#ticker-streams it makes <symbol>@bookTicker
    '''
    def __call__(self, symbols: List[symbol_t]) -> List[stream_t]:
        streams: List[stream_t] = []
        for symbol in symbols:
            streams.append(stream_t(name=f"{symbol.name.lower()}@bookTicker"))
        return streams


class BinanceWebsocketBooktickerAveragePrice(AbstractMessageDataProcessing):
    def __init__(self, storage:AbstractPriceStorage):
        self.price_storage = storage
    
    def __call__(self, message):
        '''
        According to https://docs.binance.us/#individual-symbol-ticker-streams we get sth like this:
        {
            "u":400900217,     // order book updateId
            "s":"BNBUSDT",     // symbol
            "b":"25.35190000", // best bid price
            "B":"31.21000000", // best bid qty
            "a":"25.36520000", // best ask price
            "A":"40.66000000"  // best ask qty
        }
        So, we put in object field average price ( (best bid price + best ask price )/2)
        '''
        self.price_storage.update_price(symbol_t(name=message["s"]), (float(message["a"]) + float(message["b"])) / 2)
