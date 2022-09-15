from typing import Dict, Union

from .general_part import symbol_t, AbstractPriceStorage, AbstractCachingStrategy 
from .cache_impl import NoCache

class PriceStorage(AbstractPriceStorage):

    def __init__(self, cacher:AbstractCachingStrategy=NoCache()) -> None:
        self.__prices: Dict[str, float] = {}
        self.__cacher = cacher

    def get_price(self, symbol: symbol_t) -> Union[float, None]:
        if symbol.name not in self.__prices.keys():
            raise KeyError(f"There's no data about symbol : {symbol.name}.")
        return self.__prices[symbol.name]

    def update_price(self, symbol:symbol_t, price:float) -> None:
        '''updating price. example: 
        ```
            object:AbstractPriceStorage = PriceStorage(strategy:AbstractCachingStrategy=something)
            object.update_price(symbol_t("BTCUSDT"), 25646.91 )
            price = object.get_price(symbol_t("BTCUSDT")) # 25646.91
        ```
        '''
        
        self.__cacher.save_to_cache({symbol,price})
        self.__prices.update({symbol.name:price})
        

    def get_all_prices(self) -> Dict[symbol_t, float]:
        return self.__prices
    
    def delete_price(self, symbol:symbol_t) -> None:
        result = self.__prices.pop(symbol.name, None)
        if result is None:
            raise KeyError("Trying to delete a price for something that doesn't exist.")