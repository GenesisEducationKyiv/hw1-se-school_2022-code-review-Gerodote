from typing import Dict, List

from ...general_part import AbstractPriceStorage, symbol_t
from ..general_part import (AbstractCreatorStreamsStrings,
                            AbstractMessageDataProcessing, stream_t)


class GeminiWebsocketTopOfBookCreatorStream(AbstractCreatorStreamsStrings):

    def __call__(self, symbols: List[symbol_t]) -> List[stream_t]:
        stream = "/v1/multimarketdata?symbols=" + ",".join(
            [symbol.name.upper() for symbol in symbols])
        stream += "&top_of_book=true"
        return [stream_t(stream)]


class GeminiWebsocketTopOfBookDataProcessing(AbstractMessageDataProcessing):

    def __init__(self, storage: AbstractPriceStorage):
        self.price_storage = storage

    def __call__(self, message: Dict):
        '''
            it from next messages gets price and puts it into storage.
            {"type":"update","eventId":143329393638,"timestamp":1663603023,"timestampms":1663603023472,"socket_sequence":229,"events":[{"type":"change","side":"bid","price":"1341.62","remaining":"1.7","reason":"top-of-book","symbol":"ETHUSD"}]}
            {"type":"update","eventId":143329393651,"timestamp":1663603023,"timestampms":1663603023472,"socket_sequence":230,"events":[{"type":"change","side":"ask","price":"1342.10","remaining":"4.492403","reason":"top-of-book","symbol":"ETHUSD"}]}
            {"type":"update","eventId":143329393663,"timestamp":1663603023,"timestampms":1663603023483,"socket_sequence":231,"events":[{"type":"change","side":"ask","price":"1342.09","remaining":"1.7","reason":"top-of-book","symbol":"ETHUSD"}]}
            {"type":"update","eventId":143329393665,"timestamp":1663603023,"timestampms":1663603023484,"socket_sequence":232,"events":[{"type":"change","side":"bid","price":"1341.48","remaining":"1.7","reason":"top-of-book","symbol":"ETHUSD"}]}
            {"type":"update","eventId":143329393761,"timestamp":1663603023,"timestampms":1663603023518,"socket_sequence":233,"events":[{"type":"change","side":"ask","price":"19070.50","remaining":"0.26218505","reason":"top-of-book","symbol":"BTCUSD"}]}
            {"type":"update","eventId":143329393769,"timestamp":1663603023,"timestampms":1663603023521,"socket_sequence":234,"events":[{"type":"change","side":"ask","price":"19070.46","remaining":"0.235","reason":"top-of-book","symbol":"BTCUSD"}]}
            {"type":"update","eventId":143329394076,"timestamp":1663603023,"timestampms":1663603023654,"socket_sequence":235,"events":[{"type":"change","side":"ask","price":"1342.09","remaining":"3.4","reason":"top-of-book","symbol":"ETHUSD"}]}
        '''
        for update_data in message["events"]:
            self.price_storage.update_price(symbol_t(update_data["symbol"]),
                                            float(update_data["price"]))
