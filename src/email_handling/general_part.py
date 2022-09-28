from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, EmailStr


class Email(BaseModel):
    str: EmailStr


class AbstractEmailRepo(ABC):

    @abstractmethod
    async def read_emails(self) -> List[Email]:
        raise NotImplementedError()

    @abstractmethod
    async def write_emails(self, emails: List[Email]):
        raise NotImplementedError()

    @abstractmethod
    async def is_already_exist(self, email: Email) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def add_email(self, email: Email) -> None:
        raise NotImplementedError()


class AbstractMailSender(ABC):

    @abstractmethod
    def send_plain_messages_to_emails(self,
                                      list_subscribed_emails: List[Email],
                                      subject_text: str,
                                      message_plain_text: str):
        pass


class AbstractEmailHandler(ABC):

    @abstractmethod
    async def subscribe(self, email_str: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def send_emails(self, subject_text: str,
                          message_plain_text: str) -> None:
        raise NotImplementedError()
