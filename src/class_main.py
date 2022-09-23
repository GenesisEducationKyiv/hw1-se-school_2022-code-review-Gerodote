import logging
from typing import List

import yaml


from .email_handling.mail_handler import factory_mail_handler, AbstractMailSender
from .email_handling.general_part import AbstractEmailRepo
from .email_handling.repos_emails import EmailRepoFileJSON
from .email_handling.email_handler import EmailHandler
from .price_provider.general_part import symbol_t, AbstractPriceStorage
from .price_provider.websockets.binance_websockets.binance_websocket_starter import BinanceWebsocketStarter
from .price_provider.websockets.binance_websockets.binance_data_parser import BinanceBooktickerCreatorStreams, BinanceWebsocketBooktickerAveragePrice
from .price_provider.websockets.binance_websockets.binance_stream_receiver import BinanceWebsocketStreamsReceiver
from .price_provider.websockets.how_to_use_it import start_websockets
from .price_provider.price_storage import PriceStorage
from .price_provider.cache_impl import CacheToListInMemoryAutoDelete

class BadConfig(Exception):
    pass


class MainApp:

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MainApp, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        with open("config.yaml") as file:
            logging.info("Loading configuration file 'config.yaml'")
            config = yaml.safe_load(file)
            if "gmail" in config["emails"]:
                mail_sender: AbstractMailSender = factory_mail_handler(
                    mode="gmail", **config["emails"]["gmail"])
            else:
                raise BadConfig(
                    "In config there's no 'email -> *mail_sender_service_name* ', or it's there, but not implemented in the application."
                )

            
            email_repo: AbstractEmailRepo = EmailRepoFileJSON(
                config["emails"]["file_with_emails"])
            self.__mail_handler = EmailHandler(email_repo, mail_sender)
            self.__subject: str = config["emails"]["subject"]
            self.__text_before_rate: str = config["emails"]["text_before_rate"]
            self.__text_after_rate: str = config["emails"]["text_after_rate"]


            # because there's still no support in our API for multiple subscription data.
            self.__symbol: symbol_t = symbol_t(config["symbols"]["name"][0]) 
            self.__price_storage:AbstractPriceStorage = PriceStorage(CacheToListInMemoryAutoDelete(300))
            # if was support for multiple streams, here would be ...(...(...), "stream","data").
            message_receiver = BinanceWebsocketStreamsReceiver(BinanceWebsocketBooktickerAveragePrice(self.__price_storage), None, None)            
            start_websockets([self.__symbol], BinanceBooktickerCreatorStreams(),BinanceWebsocketStarter(), message_receiver)
            
            
            
            logging.info("Configuration file loaded successfully.")

    def get_rate(self) -> float:
        task_get_price = self.__price_storage.get_price(self.__symbol)
        return task_get_price



    async def subscribe(self, email: str) -> None:
        await self.__mail_handler.subscribe(email)

    async def send_emails(self):
        await self.__mail_handler.send_emails(
            subject_text=self.__subject,
            message_plain_text=self.__text_before_rate + str(self.get_rate()) +
            self.__text_after_rate,
        )
