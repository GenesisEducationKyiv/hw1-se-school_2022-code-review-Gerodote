from typing import Callable, Union

from ..streams_receiver import GeneralWebsocketStreamsReceiver


class BinanceWebsocketStreamsReceiver(GeneralWebsocketStreamsReceiver):
    def __init__(self, data_processor: Callable,
                 key_in_message_corresponding_to_stream_name: Union[str, None],
                 key_in_message_corresponding_to_data: Union[str, None]):
        super().__init__(data_processor, key_in_message_corresponding_to_stream_name,key_in_message_corresponding_to_data)

    def __call__(self, text:str):
        super().__call__(None, text)