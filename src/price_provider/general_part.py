from typing import Union
from abc import ABC, abstractmethod



class GetterPrice(ABC):
    @abstractmethod
    def get_price(self, symbol:str) -> Union[float, None]:
        pass

