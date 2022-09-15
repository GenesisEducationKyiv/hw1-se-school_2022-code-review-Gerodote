import atexit
from typing import Callable, Dict, List, Union
from time import sleep
import logging

from binance.websocket.spot.websocket_client import (
    SpotWebsocketClient as WebsocketClient, )

from ..general_part import stream_t, AbstractWebsocketStarter


class BinanceWebsocketStarter(AbstractWebsocketStarter):
    _magic_const_url: int = 45  # len("wss://stream.binance.com:9443/stream?streams=")
    _magic_const_max_size_of_url: int = 16384  # max bytes in one url (limit of cloudflare)

    def __init__(self) -> None:
        self._websocket = WebsocketClient()
        self._websocket.start()
        atexit.register(self.__exit__)

    def __enter__(self):
        self._websocket = WebsocketClient()
        self._websocket.start()
        return self

    def __exit__(self, *args, **kwargs):
        self._websocket.stop()

    def subscribe_one_stream(
            self, stream: stream_t,
            message_handler: Callable[[Union[List, Dict]], None]) -> None:
        self._websocket.instant_subscribe(stream=stream.name,
                                          callback=message_handler)

    def subscribe_multiple_streams(
            self, streams: List[stream_t],
            message_handler: Callable[[Union[List, Dict]], None]) -> None:
        '''
        why this looks like a shit? what this do? 
        explanation: 
        There's a limitation of url length for cloudflare: no more symbols than 2^14 chars.
        So, it's adding stream-strings to url, which we send to get subscription. 
        Then do this again, and again, until every stream is subscribed.
        '''

        amount_of_subscribed_streams = 0
        while amount_of_subscribed_streams != len(streams):
            len_of_url = self._magic_const_url
            how_many_streams_in_the_url = 0
            while amount_of_subscribed_streams != range(len(streams)):
                if len_of_url + \
                    len(streams[amount_of_subscribed_streams + how_many_streams_in_the_url].name) \
                    + 1 >= self._magic_const_max_size_of_url:
                    break
                if amount_of_subscribed_streams + how_many_streams_in_the_url + 1 == len(
                        streams):
                    how_many_streams_in_the_url += 1
                    break
                how_many_streams_in_the_url += 1
                len_of_url += len(
                    streams[amount_of_subscribed_streams +
                            how_many_streams_in_the_url].name) + 1

            self._websocket.instant_subscribe(
                stream=[
                    stream.name
                    for stream in streams[amount_of_subscribed_streams:
                                          amount_of_subscribed_streams +
                                          how_many_streams_in_the_url]
                ],
                callback=message_handler,
            )
            amount_of_subscribed_streams += how_many_streams_in_the_url
            secs_to_wait = 10
            logging.info(f"waiting {secs_to_wait} secs")
            sleep(secs_to_wait)
