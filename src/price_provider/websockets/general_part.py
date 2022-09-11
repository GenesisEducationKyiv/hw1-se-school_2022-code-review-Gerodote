from pydantic.dataclasses import dataclass as pyd_dataclass
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union

@pyd_dataclass(eq=True, frozen=True)
class stream_t:
    name: str


# here could be a validation... according to https://docs.binance.us/#websocket-streams ...


class AbstractCreaterStreamsStrings(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> List[stream_t]:
        pass


class AbstractMessageDataProcessing(ABC):

    @abstractmethod
    def __call__(self, data: Union[Dict, List]) -> Any:
        pass