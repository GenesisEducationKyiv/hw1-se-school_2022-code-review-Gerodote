import logging

import yaml

from .price_provider.general_part import AbstractGetterPrice
from .price_provider.binance_websocket.getter_price_binance import PriceStorage
from .email_handling.mail_handler import factory_mail_handler, AbstractMailSender
from .email_handling.general_part import AbstractEmailRepo
from .email_handling.repos_emails import EmailRepoFileJSON
from .email_handling.email_handler import EmailHandler


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

            self.__symbol: str = config["symbols"]["name"][0]
            email_repo: AbstractEmailRepo = EmailRepoFileJSON(
                config["emails"]["file_with_emails"])
            self.__mail_handler = EmailHandler(email_repo, mail_sender)
            self.__subject: str = config["emails"]["subject"]
            self.__text_before_rate: str = config["emails"]["text_before_rate"]
            self.__text_after_rate: str = config["emails"]["text_after_rate"]

            self.__getter_price: AbstractGetterPrice = PriceStorage(
                symbol=self.__symbol)

            
            
            
            logging.info("Configuration file loaded successfully.")

    def get_rate(self) -> float:
        task_get_price = self.__getter_price.get_price(self.__symbol)
        return task_get_price

    async def subscribe(self, email: str) -> None:
        await self.__mail_handler.subscribe(email)

    async def send_emails(self):
        await self.__mail_handler.send_emails(
            subject_text=self.__subject,
            message_plain_text=self.__text_before_rate + str(self.get_rate()) +
            self.__text_after_rate,
        )
