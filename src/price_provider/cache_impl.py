from time import time

from .general_part import AbstractCachingStrategy


class NoCache(AbstractCachingStrategy):

    def __init__(self):
        pass

    def save_to_cache(self, data) -> None:
        pass

    def get_cache(self) -> None:
        return None


class CacheToListInMemoryAutoDelete(AbstractCachingStrategy):

    def __init__(self, time_upto_which_we_save_data: float = 300):
        self.__data = []
        self.__delta_time = time_upto_which_we_save_data

    def save_to_cache(self, data) -> None:
        self.__data.append({time(): data})
        self.__delete_everything_that_was_not_in_last_time()

    def get_cache(self):
        result = [list(x.values())[0] for x in self.__data]
        self.__delete_everything_that_was_not_in_last_time()
        return result

    def __delete_everything_that_was_not_in_last_time(self):
        time_now = time()
        for data in self.__data:
            if list(data.keys())[0] + self.__delta_time < time_now:
                self.__data.pop(0)


class CacheToFileNoDelete(AbstractCachingStrategy):

    def __init__(self, filename: str = "cache_prices.txt"):
        self.__filename_to_save_data = filename

    def save_to_cache(self, data) -> None:
        with open(self.__filename_to_save_data, mode='a') as file:
            file.write(str(data))

    def get_cache(self):
        result = None
        with open(self.__filename_to_save_data, 'r') as file:
            result = file.read()
        return result
