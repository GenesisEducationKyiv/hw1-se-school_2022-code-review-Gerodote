import base64
import os
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class BasicGmailAPI:
    def __init__(self, client_secret_file, api_name, api_version, scopes):
        self._CLIENT_SECRET_FILE = client_secret_file
        self._API_SERVICE_NAME = api_name
        self._API_VERSION = api_version
        self._SCOPES = scopes

        cred = None

        pickle_file = f"token_{self._API_SERVICE_NAME}_{self._API_VERSION}.pickle"

        if os.path.exists(pickle_file):
            with open(pickle_file, "rb") as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._CLIENT_SECRET_FILE, self._SCOPES
                )
                cred = flow.run_local_server()

            with open(pickle_file, "wb") as token:
                pickle.dump(cred, token)

        try:
            self._service = build(
                self._API_SERVICE_NAME, self._API_VERSION, credentials=cred
            )
            print(self._API_SERVICE_NAME, "service created successfully")
        except Exception as e:
            print("Unable to connect.")
            print(e)
            self._service = None

    def send_message_plain_text(self, to, subject, message_text):
        emailMsg = message_text
        mimeMessage = MIMEMultipart()
        mimeMessage["to"] = to
        mimeMessage["subject"] = subject
        mimeMessage.attach(MIMEText(emailMsg, "plain"))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = (
            self._service.users()
            .messages()
            .send(userId="me", body={"raw": raw_string})
            .execute()
        )
        print(message)
