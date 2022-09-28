from os import remove
from time import sleep

from src.price_provider.cache_impl import CacheToListInMemoryAutoDelete, CacheToFileNoDelete

def test_cache_to_file():
    filename:str = "test_cache_to_file.txt"
    cacher = CacheToFileNoDelete(filename)
    cacher.save_to_cache("sth")
    sth = None
    with open(filename,"r") as f:
        sth = f.read()
    try:
        assert sth == "sth"
    finally:
        remove(filename)

def test_cache_to_list_in_memory():
    cacher = CacheToListInMemoryAutoDelete()
    cacher.save_to_cache("sth")
    sth = cacher.get_cache()
    assert sth[0] == "sth"
    
def test_cache_to_list_in_memory_2():
    cacher = CacheToListInMemoryAutoDelete(5)
    cacher.save_to_cache("sth")
    sleep(6)
    cacher.save_to_cache("sth2")
    sth = cacher.get_cache()
    assert sth[0] == "sth2"
    
        