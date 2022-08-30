from abc import ABC, abstractmethod

import gmail_API


class AbstractMailHandler(ABC):
    @abstractmethod
    def send_plain_messages_to_emails(self,
                                      list_subscribed_emails,
                                      subject_text,
                                      message_plain_text):
        pass
    
    
class GmailHandler(AbstractMailHandler):
    def __init__(self,
                 client_secret_file='client_secret.json',
                 api_name='gmail',
                 api_version='v1', 
                 scopes=['https://www.googleapis.com/auth/gmail.send']
                 ):
        self._gmail_client = gmail_API.BasicGmailAPI(client_secret_file,
                                                       api_name,
                                                       api_version,
                                                       scopes)
        
    def send_plain_messages_to_emails(self,
                                            list_subscribed_emails,
                                            subject_text, message_plain_text):
        for email in list_subscribed_emails:
            self._gmail_client.send_message_plain_text(
                to=email,
                subject=subject_text,
                message_text=message_plain_text
            )
        
def factory_mail_handler(mode='gmail', *args, **kwargs) -> AbstractMailHandler:
        '''
        Use any mode from: "gmail", "SMTP"
        '''
        if mode == 'gmail':
            return GmailHandler(*args, **kwargs)
        # if mode == 'SMTP':
        #     return SMTP_handler(*args, **kwargs)
        raise KeyError(f"such mode either don't exist or didn't implemented.")

        
if __name__ == "__main__":
    print("Executing initialization of gmail account.")
    print("!!! WARNING: don't delete this file after configuring gmail API, "+\
        "because this file is also used to run the gmail API on server.")
    gmail_client = GmailHandler()            
            