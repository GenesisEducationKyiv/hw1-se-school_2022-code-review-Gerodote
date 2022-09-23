import ssl
import websocket
import _thread as thread
from typing import Callable, Optional, Union, List, Dict


from .general_part import AbstractWebsocketStarter, stream_t

def general_on_error(ws, error):
    print(error)

def general_on_open(ws):
    def run(*args):
        ws.send("Hello there!")
    thread.start_new_thread(run,())
    
def general_on_close(ws):
    print("### closed ###")

class WebsocketStarter(AbstractWebsocketStarter):
    def __init__(self, base_wss_url:str, splitter:str="/", max_size_of_url:int=16384):
        '''an general WebsocketStarter'''
        self.__max_size_of_url:int = max_size_of_url
        self.__base_wss_url:str = base_wss_url
        self.__splitter:str = splitter
        
    def subscribe_one_stream(self, 
                             stream: stream_t, 
                             on_message: Callable[[Union[List, Dict]], None],
                             on_error: Optional[Callable[[Union[List, Dict]],None]]=general_on_error,
                             on_close: Optional[Callable[[Union[List, Dict]],None]]=general_on_close,
                             on_open: Optional[Callable[[Union[List, Dict]],None]]=general_on_open
                             ):
        print(f"Connecting to {self.__base_wss_url + stream.name}")
        self.__ws = websocket.WebSocketApp(
            self.__base_wss_url + self.__splitter + stream.name,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
            )
        self.__ws.on_open = on_open
        self.__ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def subscribe_multiple_streams(self, 
                                   streams: List[stream_t], 
                                   on_message: Callable[[Union[List, Dict]], None],
                                   on_error: Optional[Callable[[Union[List, Dict]],None]]=general_on_error,
                                   on_close: Optional[Callable[[Union[List, Dict]],None]]=general_on_close,
                                   on_open: Optional[Callable[[Union[List, Dict]],None]]=general_on_open
                                   ) -> None:
        # here should be twisted package use. up to max_size_of_url this works, then this doesn't work.
        self.subscribe_one_stream(self.__splitter.join([stream.name for stream in streams]),
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close,
                                  on_open=on_open)
                                  
                                  