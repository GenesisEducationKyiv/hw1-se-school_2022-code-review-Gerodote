from pydantic.dataclasses import dataclass as pyd_dataclass
from abc import ABC, abstractmethod
from typing import Any, Callable, List, Dict, Union

@pyd_dataclass(eq=True, frozen=True)
class stream_t:
    name: str
# here could be a validation... according to https://docs.binance.us/#websocket-streams ...


class AbstractCreatorStreamsStrings(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Union[List[stream_t], stream_t]:
        raise NotImplementedError()


class AbstractMessageDataProcessing(ABC):

    @abstractmethod
    def __call__(self, data: Union[Dict, List]) -> Any:
        raise NotImplementedError()

class AbstractWebsocketStarter(ABC):
    @abstractmethod
    def subscribe_one_stream(self, stream:stream_t, message_handler:Callable[[Union[List, Dict]], None]):
        raise NotImplementedError()
    
    @abstractmethod
    def subscribe_multiple_streams(self, streams: List[stream_t],
            message_handler: Callable[[Union[List, Dict]], None]) -> None:
        raise NotImplementedError()
    
class AbstractWebsocketMessageReceiver(ABC):
    @abstractmethod
    def __call__(self, message:Dict) -> None:
        raise NotImplementedError()
