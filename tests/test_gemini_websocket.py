from typing import List
from time import sleep
import json

from src.price_provider.cache_impl import CacheToFileNoDelete, NoCache
from src.price_provider.general_part import symbol_t, AbstractPriceStorage
from src.price_provider.websockets.general_part import AbstractWebsocketStarter, stream_t, AbstractCreatorStreamsStrings
from src.price_provider.websockets.gemini_websockets.gemini_websocket_starter import GeminiWebsocketStarter
from src.price_provider.websockets.gemini_websockets.gemini_data_parser import GeminiTopOfBookCreatorStream, GeminiTopOfBookDataProcessing
from src.price_provider.websockets.streams_receiver import GeneralWebsocketStreamsReceiver
from src.price_provider.price_storage import PriceStorage


def test_gemini_check_string():
    sth = GeminiTopOfBookCreatorStream()
    sth2 = sth.__call__([symbol_t("BTCUSD"), symbol_t("ETHUSD")])
    assert sth2 == stream_t("/v1/multimarketdata?symbols=BTCUSD,ETHUSD&top_of_book=true")
    
def test_gemini_check_data_processor():
    sth = GeminiTopOfBookDataProcessing(PriceStorage(NoCache()))
    sth.__call__(message=json.loads('{"type":"update","eventId":143329393665,"timestamp":1663603023,"timestampms":1663603023484,"socket_sequence":232,"events":[{"type":"change","side":"bid","price":"1341.48","remaining":"1.7","reason":"top-of-book","symbol":"ETHUSD"}]}'))
    assert sth.price_storage.get_price(symbol_t("ETHUSD")) is not None
    
def test_gemini_ws_top_of_book():
    ''' 
    Just try run this test by itself without others. 
    for example : pytest -k gemini
    This command will run only tests with this substring.
   '''
    symbols_strings = ["ETHUSD", "BTCUSD"]

    symbols_lst: List[symbol_t] = [
        symbol_t(name=symbol) for symbol in symbols_strings
    ]
    stream_creator: AbstractCreatorStreamsStrings = GeminiTopOfBookCreatorStream(
    )
    streams: stream_t = stream_creator(symbols=symbols_lst)
    data_processor: GeminiTopOfBookDataProcessing = GeminiTopOfBookDataProcessing(
        PriceStorage(CacheToFileNoDelete("cache_prices.txt")))
    ws_starter: AbstractWebsocketStarter = GeminiWebsocketStarter()

    ws_starter.subscribe_one_stream(
        streams,
        message_handler=GeneralWebsocketStreamsReceiver(data_processor, None,
                                                    None))

    for_do_while: bool = True
    count_how_many_times_checked = 0
    while (for_do_while):
        print(count_how_many_times_checked)
        sleep(15)
        for symbol in symbols_lst:
            try:
                data_processor.price_storage.get_price(symbol=symbol)
            except KeyError:
                count_how_many_times_checked += 1
                break
            for_do_while = False
        if count_how_many_times_checked > 2:
            for_do_while = False

    assert data_processor.price_storage.get_price(
        symbol_t("ETHUSD")) is not None

if __name__ == "__main__":
    test_gemini_ws_top_of_book()