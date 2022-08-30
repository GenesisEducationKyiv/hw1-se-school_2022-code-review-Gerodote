import asyncio
import logging

from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_client import (
    SpotWebsocketClient as WebsocketClient,
)

config_logging(logging, logging.DEBUG)


class book_ticker_price_binance:
    def __init__(self, symbols=None, symbol=None):
        if symbols != None and symbol != None:
            raise ValueError(
                "Getter_price_binance: Please, write or symbols OR symbol."
            )
        if symbols == None and symbol == None:
            raise TypeError("Getter_price_binance: Please, enter any param.")
        self._websocket_client = WebsocketClient()
        self._websocket_client.start()
        self._message = None
        self._prices = {}
        self._subscribed_symbols = []
        if symbols != None:
            self._subscribed_symbols = symbols
            self._symbols_in_lower_case = [symbol.lower() for symbol in symbols]
            self._streams = [
                f"{symbol}@bookTicker" for symbol in self._symbols_in_lower_case
            ]
            self._websocket_client.instant_subscribe(
                stream=self._streams, callback=self.streams_handler
            )

        if symbol != None:
            self._subscribed_symbols += [symbol]
            self._symbol_in_lower_case = symbol.lower()
            self._websocket_client.instant_subscribe(
                stream=f"{self._symbol_in_lower_case}@bookTicker",
                callback=self.stream_handler,
            )

    def __del__(self):
        self._websocket_client.stop()

    def stop_ws(self):
        self._websocket_client.stop()

    def stream_handler(self, message):
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

    def streams_handler(self, message):
        self._message = message
        self.stream_handler(message=message["data"])
