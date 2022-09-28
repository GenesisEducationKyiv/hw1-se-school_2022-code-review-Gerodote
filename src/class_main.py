import logging
from typing import List

import yaml
from pydantic import ValidationError

from .email_handling.email_handler import EmailHandler
from .email_handling.general_part import (AbstractEmailHandler,
                                          AbstractEmailRepo)
from .email_handling.mail_sender import (AbstractMailSender,
                                         factory_mail_handler)
from .email_handling.repos_emails import EmailRepoFileJSON
from .price_provider.binance_provider import BinanceWebsocketBooktickerAveragePriceProvider
from .price_provider.gemini_provider import GeminiWebsocketTopOfBookPriceProvider
from .price_provider.general_part import AbstractPriceProvider, symbol_t


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
            self.__mail_handler: AbstractEmailHandler = EmailHandler(
                email_repo, mail_sender)
            self.__subject: str = config["emails"]["subject"]
            self.__text_before_rate: str = config["emails"]["text_before_rate"]
            self.__text_after_rate: str = config["emails"]["text_after_rate"]

            try:
                self.__symbol = symbol_t(config["symbols"]["name"][0])
            except ValidationError as e:
                raise BadConfig(
                    f"symbol is written in wrong way. Details if they exist: {e.__str__()}"
                )
            if "env" in config:
                if config["env"]["CRYPTO_CURRENCY_PROVIDER"] == "gemini":
                    self.__price_provider: AbstractPriceProvider = GeminiWebsocketTopOfBookPriceProvider(
                        self.__symbol)
            else:  # if config["env"]["CRYPTO_CURRENCY_PROVIDER"] == "binance":
                self.__price_provider: AbstractPriceProvider = BinanceWebsocketBooktickerAveragePriceProvider(
                    self.__symbol)

            logging.info("Configuration file loaded successfully.")

    def get_rate(self) -> float:
        task_get_price = self.__price_provider.get_price(self.__symbol)
        return task_get_price

    async def subscribe(self, email: str) -> None:
        await self.__mail_handler.subscribe(email)

    async def send_emails(self):
        await self.__mail_handler.send_emails(
            subject_text=self.__subject,
            message_plain_text=self.__text_before_rate + str(self.get_rate()) +
            self.__text_after_rate,
        )
