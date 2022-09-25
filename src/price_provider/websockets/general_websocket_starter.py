import ssl
import threading
from typing import Callable, Dict, List, Optional, Union

from websocket import WebSocketApp  # , enableTrace # for debugging

from .general_part import AbstractWebsocketStarter, stream_t


def general_on_error(ws, error):
    print(f"Connection to a websocket got an error: {error}")


def general_on_open(ws):
    print("Connection to a websocket opened.")


def general_on_close(ws, close_status_code, close_msg):
    print("Connection to a websocket closed.")
    print(close_status_code, close_msg)


class WebsocketStarter(AbstractWebsocketStarter):

    def __init__(self,
                 base_wss_url: str,
                 splitter: str = "/",
                 max_size_of_url: int = 16384):
        '''an general WebsocketStarter'''
        self.__max_size_of_url: int = max_size_of_url
        self.__base_wss_url: str = base_wss_url
        self.__splitter: str = splitter
        # enableTrace(True) #for debugging

    def subscribe_one_stream(
        self,
        stream: stream_t,
        on_message: Callable[[Union[List, Dict]], None],
        on_error: Optional[Callable[[Union[List, Dict]],
                                    None]] = general_on_error,
        on_close: Optional[Callable[[Union[List, Dict]],
                                    None]] = general_on_close,
        on_open: Optional[Callable[[Union[List, Dict]],
                                   None]] = general_on_open):
        self.__url = self.__base_wss_url + stream.name
        print(f"Connecting to {self.__url}")

        self.__ws = WebSocketApp(self.__url,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close,
                                 on_open=on_open)
        self.__ws.on_open = on_open

        def ws_on_background(ws):
            self.__ws.run_forever(
                sslopt={"cert_reqs": ssl.CERT_NONE}
            )  # want more speed? here `skip_utf8_validation=True` and `pip install wsaccel`

        threading.Thread(target=ws_on_background,
                         args=(self.__ws, ),
                         daemon=True).start()

    def subscribe_multiple_streams(
        self,
        streams: List[stream_t],
        on_message: Callable[[Union[List, Dict]], None],
        on_error: Optional[Callable[[Union[List, Dict]],
                                    None]] = general_on_error,
        on_close: Optional[Callable[[Union[List, Dict]],
                                    None]] = general_on_close,
        on_open: Optional[Callable[[Union[List, Dict]],
                                   None]] = general_on_open
    ) -> None:
        # future TODO: if streams are a lot, use or _thread,
        # or twisted or anything like this to increase amount of endpoints.
        # then, check code for binance websocket starter.
        # there's an interesting code to limit url size to a max_size_of_url.

        # here should be twisted package use. up to max_size_of_url this works, then this doesn't work.
        self.subscribe_one_stream(self.__splitter.join(
            [stream.name for stream in streams]),
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close,
                                  on_open=on_open)
