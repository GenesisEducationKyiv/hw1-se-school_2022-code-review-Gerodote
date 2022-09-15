from typing import Dict, Union
from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass as pyd_dataclass


@pyd_dataclass(eq=True, frozen=True)
class symbol_t():
    '''like "BTCUSDT", "BTCUAH" ...'''
    name: str


@pyd_dataclass(eq=True, frozen=True)
class currency_t():
    '''like "BTC", "USDT", "UAH" ...'''
    name: str


class AbstractPriceStorage(ABC):
    @abstractmethod
    def get_price(self, symbol: symbol_t) -> Union[float, None]:
        raise NotImplementedError()

    @abstractmethod
    def update_price(self, symbol:symbol_t, price: float) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_price(self, symbol: symbol_t) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_prices(self) -> Dict[symbol_t, float]:
        raise NotImplementedError()
    
class AbstractCachingStrategy(ABC):
    @abstractmethod
    def save_to_cache(self, data) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_cache(self):
        raise NotImplementedError()
