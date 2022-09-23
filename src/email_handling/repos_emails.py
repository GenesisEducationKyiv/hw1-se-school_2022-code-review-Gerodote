import json
import logging
import os
from shutil import copy2
from typing import List

import aiofiles
from pydantic import error_wrappers

from .general_part import AbstractEmailRepo, Email


class EmailRepoFileJSON(AbstractEmailRepo):

    def __init__(self, filename_for_and_with_emails: str) -> None:
        self._filename_with_emails = filename_for_and_with_emails

    async def read_emails(self) -> List[Email]:
        data = []
        if os.path.exists(self._filename_with_emails):
            async with aiofiles.open(self._filename_with_emails,
                                     "r") as subscribed_emails:
                raw_data = await subscribed_emails.read()
                try:
                    not_validated_yet_data = json.loads(raw_data)
                    data = [
                        Email(str=data_piece)
                        for data_piece in not_validated_yet_data
                    ]
                except json.JSONDecodeError:
                    logging.warning(
                        f"File {self._filename_with_emails} is not JSON.")
                    self._backup_file_to_file()
                except error_wrappers.ValidationError:
                    logging.warning(
                        f"Data in file {self._filename_with_emails} is not valid."
                    )
                    self._backup_file_to_file()
        return data

    async def write_emails(self, data:List[Email]):
        async with aiofiles.open(self._filename_with_emails,
                                 "w") as subscribed_emails:
            unwrapped_data:List[str] = [email.str for email in data]
            await subscribed_emails.write(json.dumps(unwrapped_data))

    async def is_already_exist(self, email: Email) -> bool:
        data = await self.read_emails()
        if email in data:
            return True
        return False

    async def add_email(self, email: Email) -> None:
        data = await self.read_emails()
        data.append(email)
        await self.write_emails(data)

    def _backup_file_to_file(self):
        # if was "sth.sth2.sth3.json", it will be saved to "sth.sth2.sth3__saved.json"
        copy_destination = ((".".join(
            ((str(self._filename_with_emails)).split("."))[:-1])) +
                            "__saved." +
                            str(self._filename_with_emails).split(".")[-1])
        logging.warning(
            f"Copying file {self._filename_with_emails} to {copy_destination}")
        copy2(self._filename_with_emails, copy_destination)
