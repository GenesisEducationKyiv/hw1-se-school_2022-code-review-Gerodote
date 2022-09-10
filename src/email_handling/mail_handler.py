from abc import ABC, abstractmethod
from typing import List

from .general_part import Email
from .gmail_API import BasicGmailAPI


class AbstractMailSender(ABC):
    @abstractmethod
    def send_plain_messages_to_emails(self,
                                      list_subscribed_emails:List[Email],
                                      subject_text:str,
                                      message_plain_text:str):
        pass
    
    
class GmailSender(AbstractMailSender):
    def __init__(self,
                 client_secret_file='client_secret.json',
                 api_name='gmail',
                 api_version='v1', 
                 scopes=['https://www.googleapis.com/auth/gmail.send']
                 ):
        self._gmail_client = BasicGmailAPI(client_secret_file,
                                                       api_name,
                                                       api_version,
                                                       scopes)
        
    def send_plain_messages_to_emails(self,
                                      list_subscribed_emails:List[Email],
                                      subject_text:str, 
                                      message_plain_text:str):
        for email in list_subscribed_emails:
            self._gmail_client.send_message_plain_text(
                to=email.str,
                subject=subject_text,
                message_text=message_plain_text
            )
        
def factory_mail_handler(mode='gmail', *args, **kwargs) -> AbstractMailSender:
        '''
        Use any mode from: "gmail", "SMTP"
        '''
        if mode == 'gmail':
            return GmailSender(*args, **kwargs)
        raise KeyError(f"such mode either don't exist or didn't implemented.")

        
if __name__ == "__main__":
    print("Executing initialization of gmail account.")
    print("!!! WARNING: don't delete this file after configuring gmail API, "+\
        "because this file is also used to run the gmail API on server.")
    gmail_client = GmailSender()            
            