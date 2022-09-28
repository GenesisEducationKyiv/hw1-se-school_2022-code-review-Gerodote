import aiofiles

from .general_part import AbstractEmailHandler, AbstractEmailRepo, Email
from .mail_sender import AbstractMailSender


class AlreadyExist(Exception):
    pass


class EmailHandler(AbstractEmailHandler):

    def __init__(self, email_repo: AbstractEmailRepo,
                 mail_sender: AbstractMailSender):
        self.__mail_sender = mail_sender
        self.__email_repo = email_repo

    async def subscribe(self, email_str: str) -> None:
        email_validated: Email = Email(
            str=email_str)  # can raise pydantic.error_wrappers.ValidationError
        if await self.__email_repo.is_already_exist(email_validated):
            raise AlreadyExist("This email already subscribed.")
        await self.__email_repo.add_email(email_validated)

    async def send_emails(self, subject_text: str, message_plain_text: str):
        list_subscribed_emails = await self.__email_repo.read_emails()
        self.__mail_sender.send_plain_messages_to_emails(
            list_subscribed_emails=list_subscribed_emails,
            subject_text=subject_text,
            message_plain_text=message_plain_text,
        )
