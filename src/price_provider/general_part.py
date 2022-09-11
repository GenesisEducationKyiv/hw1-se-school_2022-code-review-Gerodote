from typing import Union
from abc import ABC, abstractmethod

class AbstractGetterPrice(ABC):
    @property
    @abstractmethod
    def price(self, symbol:str) -> Union[float, None]:
        pass

