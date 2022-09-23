from typing import Callable, Union, List, Dict

from ..general_part import AbstractWebsocketStarter, stream_t
from ..general_websocket_starter import WebsocketStarter

# def on_error_exception(ws, msg):
#     print(f"sth bad: {msg}")
    
class GeminiWebsocketStarter(AbstractWebsocketStarter):
    def __init__(self) -> None:
        self.__websocket_starter = WebsocketStarter("wss://api.gemini.com")
        
    def subscribe_one_stream(self, stream: stream_t, message_handler: Callable[[Union[List, Dict]], None]):
        self.__websocket_starter.subscribe_one_stream(stream, on_message=message_handler)
        
    def subscribe_multiple_streams(self, streams: List[stream_t], message_handler: Callable[[Union[List, Dict]], None]) -> None:
        self.__websocket_starter.subscribe_multiple_streams(streams, on_message=message_handler)
        