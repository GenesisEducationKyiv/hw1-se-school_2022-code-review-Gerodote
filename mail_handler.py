import gmail_API

from abc import ABC, abstractmethod

class Abstract_mail_handler(ABC):
    @abstractmethod
    def send_plain_messages_to_emails(self,
                                            list_subscribed_emails,
                                            subject_text,
                                            message_plain_text):
        pass
    
    
class gmail_handler(Abstract_mail_handler):
    def __init__(self,
                 client_secret_file='client_secret.json',
                 api_name='gmail',
                 api_version='v1', 
                 scopes=['https://www.googleapis.com/auth/gmail.send']
                 ):
        self._gmail_client = gmail_API.basic_gmail_api(client_secret_file,
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
        
def factory_mail_handler(mode='gmail', *args, **kwargs) -> Abstract_mail_handler:
        '''
        Use any mode from: "gmail", "SMTP"
        '''
        if mode == 'gmail':
            return gmail_handler(*args, **kwargs)
        # if mode == 'SMTP':
        #     return SMTP_handler(*args, **kwargs)
        raise KeyError(f"such mode either don't exist or didn't implemented.")

        
            
            