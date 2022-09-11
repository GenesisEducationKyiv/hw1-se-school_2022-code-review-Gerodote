from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union

from ..general_part import AbstractGetterPrice

class symbol_t(BaseModel):
    '''like "BTCUSDT", "BTCUAH" ...'''
    name: str
# maybe validation?

class currency_t(BaseModel):
    '''like "BTC", "USDT", "UAH" ...'''
    name: str


class stream_t(BaseModel):
    name: str
# here could be a validation... according to https://docs.binance.us/#websocket-streams


class AbstractSetPrice(ABC):
    @property.setter
    @abstractmethod
    def price(self, price:float) -> None:
        pass

class AbstractPriceGetterSetter(AbstractGetterPrice, AbstractSetPrice):
    pass

class AbstractCreaterStreamsStrings(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> List[stream_t]:
        pass
    
class AbstractMessageDataProcessing(ABC):
    @abstractmethod
    def process_data(self, data:Union[Dict, List]) -> Any:
        pass