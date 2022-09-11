from typing import Dict, Union

from .general_part import AbstractSetPrice, symbol_t
from ..general_part import AbstractGetterPrice


class PriceStorage(AbstractSetPrice, AbstractGetterPrice):

    def __init__(self) -> None:
        self.__prices: Dict[symbol_t, float] = {}

    @property
    def price(self, symbol:symbol_t) -> Union[float, None]:
        if symbol not in self.__prices:
            raise KeyError(f"There's no data about symbol : {symbol.name}.")
        return self.__prices[symbol]

    @price.setter
    def price(self, symbol_t, float) -> None:
        self.__prices[symbol_t] = float
