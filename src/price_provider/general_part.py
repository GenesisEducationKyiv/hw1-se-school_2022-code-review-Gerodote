from typing import Union
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
        pass

    @abstractmethod
    def set_price(self, symbol:symbol_t, price: float) -> None:
        pass
