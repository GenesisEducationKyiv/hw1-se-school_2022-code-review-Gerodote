from typing import Dict, Union

from ..general_part import symbol_t, AbstractPriceStorage


class PriceStorage(AbstractPriceStorage):

    def __init__(self) -> None:
        self.__prices: Dict[str, float] = {}

    def get_price(self, symbol: symbol_t) -> Union[float, None]:
        if symbol.name not in self.__prices.keys():
            raise KeyError(f"There's no data about symbol : {symbol.name}.")
        return self.__prices[symbol.name]

    def set_price(self, symbol:symbol_t, price:float) -> None:
        self.__prices.update({symbol.name:price})
