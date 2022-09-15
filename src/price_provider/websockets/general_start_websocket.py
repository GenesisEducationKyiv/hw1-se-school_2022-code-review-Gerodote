from typing import List

from ..general_part import symbol_t
from .general_part import stream_t, AbstractCreaterStreamsStrings, AbstractCreaterStreamsStrings, AbstractWebsocketStarter, AbstractWebsocketMessageReceiver

def start_websockets(symbols:List[symbol_t], 
                     streams_name_creator:AbstractCreaterStreamsStrings, 
                     websocket_net_handler:AbstractWebsocketStarter,
                     websocket_message_receiver:AbstractWebsocketMessageReceiver
                     ) -> None:
    streams: List[stream_t] = streams_name_creator(symbols=symbols)
    if len(streams) == 1:
        websocket_net_handler.subscribe_one_stream(streams[0], websocket_message_receiver)
    else:
        websocket_net_handler.subscribe_multiple_streams(streams, websocket_message_receiver) 
