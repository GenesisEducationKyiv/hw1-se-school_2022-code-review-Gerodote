from typing import List
from pydantic import BaseModel, EmailStr
from abc import ABC, abstractmethod


class Email(BaseModel):
    str: EmailStr


class AbstractEmailRepo(ABC):

    @abstractmethod
    async def read_emails(self) -> List[Email]:
        pass

    @abstractmethod
    async def write_emails(self, emails: List[Email]):
        pass

    @abstractmethod
    async def is_already_exist(self, email: Email) -> bool:
        pass

    @abstractmethod
    async def add_email(self, email: Email) -> None:
        pass