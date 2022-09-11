from typing import Dict, Union

from ..general_part import symbol_t, AbstractPriceStorage


class PriceStorage(AbstractPriceStorage):

    def __init__(self) -> None:
        self.__prices: Dict[symbol_t, float] = {}

    def get_price(self, symbol: symbol_t) -> Union[float, None]:
        if symbol not in self.__prices:
            raise KeyError(f"There's no data about symbol : {symbol.name}.")
        return self.__prices[symbol]

    def set_price(self, symbol:symbol_t, price:float) -> None:
        self.__prices[symbol] = price
