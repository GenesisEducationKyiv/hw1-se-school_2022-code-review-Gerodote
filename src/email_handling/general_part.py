from typing import List
from pydantic import BaseModel, EmailStr
from abc import ABC, abstractmethod


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