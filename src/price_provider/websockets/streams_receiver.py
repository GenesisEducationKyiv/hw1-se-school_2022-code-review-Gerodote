from time import time
from typing import Callable, Dict, Union

from .general_part import AbstractWebsocketMessageReceiver


class WebsocketStreamsReceiver(AbstractWebsocketMessageReceiver):
    __connected_streams = []
    __dict_connected_streams_time = {}
    delta_time = 10  # secs

    def __init__(self, data_processor: Callable,
                 key_in_message_corresponding_to_stream_name: Union[str, None],
                 key_in_message_corresponding_to_data: Union[str, None]):
        self.__data_handler = data_processor
        self.__key_in_message_corresponding_to_stream_name = key_in_message_corresponding_to_stream_name
        self.__key_in_message_corresponding_to_data = key_in_message_corresponding_to_data

    def __call__(self, message: Dict):
        '''
        At this moment the function is expected to get a message the way below.
        This function can do sth when process of receiving data is only in the beginning.
        When it gets data, it passes the baton to handler_message_data.
        It expects to send next messages to data handler:
        {'stream': 'srmbtc@depth20@100ms', ...sth... }
        or {...}
        
        '''
        if 'result' in message.keys():
            print(f"Connecting data: {message}", end=' ')
        else:
            if self.__key_in_message_corresponding_to_stream_name is not None:
                if message[
                        self.
                        __key_in_message_corresponding_to_stream_name] not in self.__connected_streams:
                    self.__connected_streams.append(message[
                        self.__key_in_message_corresponding_to_stream_name])
                self.__dict_connected_streams_time.update({
                    message[self.__key_in_message_corresponding_to_stream_name]:
                    time()
                })
                self.__data_handler(
                    message[self.__key_in_message_corresponding_to_data])
            else:
                self.__connected_streams.append("a_stream")
                self.__dict_connected_streams_time.update({"a_stream": time()})
                self.__data_handler(message)

    @classmethod
    def get_info_about_connected_streams(cls) -> str:
        quantity_of_streams_that_are_updated_by_last_delta_time = 0
        time_now = time()
        for key_symbol in cls.__dict_connected_streams_time:
            if time_now - cls.__dict_connected_streams_time[
                    key_symbol] < cls.delta_time:
                quantity_of_streams_that_are_updated_by_last_delta_time += 1
        return f"Connected streams: {len(cls.__connected_streams)} ; Quantity of streams updated by last {cls.delta_time} secs: {quantity_of_streams_that_are_updated_by_last_delta_time}"
