import os
import json
import asyncio
from shutil import copy2

import aiofiles

class EmailRepo():
    def __init__(self, filename_for_and_with_emails:str) -> None:
        self._filename_with_emails = filename_for_and_with_emails
        
    async def _read_file_with_emails(self):
        data = []
        if os.path.exists(self._filename_with_emails):
            async with aiofiles.open(self._file_with_emails, "r") as subscribed_emails:
                raw_data = await subscribed_emails.read()
                try:
                    data = json.loads(raw_data)
                except json.JSONDecodeError:
                    # if was "sth.sth2.sth3.json", it will be saved to "sth.sth2.sth3__saved.json"
                    copy_destination = (
                        (".".join(((str(self._filename_with_emails)).split("."))[:-1]))
                        + "__saved."
                        + str(self._filename_with_emails).split(".")[-1]
                    )
                    print(
                        f"!!! File {self._filename_with_emails} is broken. Copying it to {copy_destination}"
                    )
                    copy2(self._filename_with_emails, copy_destination)
        return data

    async def _write_file_with_emails(self, data):
        async with aiofiles.open(self._filename_with_emails, "w") as subscribed_emails:
            await subscribed_emails.write(json.dumps(data))
            
    