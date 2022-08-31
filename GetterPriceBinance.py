import asyncio
import logging

from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_client import (
    SpotWebsocketClient as WebsocketClient,
)

config_logging(logging, logging.DEBUG)


class BookTickerPriceBinance:
    def __init__(self, symbols=None, symbol=None):
        if symbols is not None and symbol is not None:
            raise ValueError(
                "Getter_price_binance: Please, write or symbols OR symbol."
            )
        if symbols is None and symbol is None:
            raise TypeError("Getter_price_binance: Please, enter any param.")
        self._message = None
        self._prices = {}        
        self._subscribed_symbols = []
        
        self._websocket_client = WebsocketClient()
        self._websocket_client.start()
        
        if symbols is not None:
            self._subscribed_symbols = symbols
            self.start_combined_streams()
            
        if symbol is not None:
            self._subscribed_symbols += [symbol]
            self.start_a_raw_stream()

    def _start_combined_streams(self):
        self._symbols_in_lower_case = [symbol.lower() for symbol in self._subscribed_symbols]
        self._streams = [
            f"{symbol}@bookTicker" for symbol in self._symbols_in_lower_case
        ]
        self._websocket_client.instant_subscribe(
            stream=self._streams, callback=self.handler_of_streams
        )

    def _start_raw_stream(self): 
        self._symbol_in_lower_case = self._subscribed_symbols[0].lower()
        self._websocket_client.instant_subscribe(
            stream=f"{self._symbol_in_lower_case}@bookTicker",
            callback=self.handler_of_a_stream_bookTicker,
        )

    

    def __del__(self):
        self._websocket_client.stop()

    def stop_ws(self):
        self._websocket_client.stop()

    def handler_of_a_stream_bookTicker(self, message):
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
        self._prices.update(
            {message["s"]: (float(self._message["a"]) + float(self._message["b"])) / 2}
        )

    async def get_price(self, symbol):
        if symbol not in self._subscribed_symbols:
            raise KeyError(f"You haven't subscribed getting {symbol}.")
        if symbol in self._prices.keys():
            return self._prices[symbol]
        else:
            return None
            
    def get_all_prices(self):
        return self._prices

    def handler_of_streams(self, message):
        self._message = message
        self.handler_of_a_stream_bookTicker(message=message["data"])
