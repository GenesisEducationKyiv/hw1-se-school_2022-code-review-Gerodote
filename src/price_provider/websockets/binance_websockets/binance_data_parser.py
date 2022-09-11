from typing import List

from ..general_part import AbstractCreaterStreamsStrings, AbstractMessageDataProcessing, symbol_t, stream_t


class BinanceBooktickerCreaterStreams(AbstractCreaterStreamsStrings):

    def __call__(symbols: List[symbol_t]) -> List[stream_t]:
        streams: List[stream_t] = []
        for symbol in symbols:
            streams.append(stream_t(f"{symbol.name.lower()}@bookticker"))
        return streams


class BinanceWebsocketBooktickerAveragePrice(AbstractMessageDataProcessing):

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
        self._message = message
        return {
            symbol_t(name=message["s"]):
            (float(self._message["a"]) + float(self._message["b"])) / 2
        }
