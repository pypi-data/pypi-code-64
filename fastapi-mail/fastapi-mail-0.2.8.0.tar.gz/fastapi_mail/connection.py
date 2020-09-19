
from fastapi_mail.config import  ConnectionConfig
from fastapi_mail.errors import ConnectionErrors, PydanticClassRequired
from pydantic import BaseSettings  as Settings
import aiosmtplib



class Connection:
    '''
    Manages Connection to provided email service with its credentials
    '''


    def __init__(self,settings: ConnectionConfig ):

        if not issubclass(settings.__class__,Settings):
            raise  PydanticClassRequired('''Email configuruation should be provided from ConnectionConfig class, check example below:
         \nfrom fastmail import ConnectionConfig  \nconf = Connection(\nMAIL_USERNAME = "your_username",\nMAIL_PASSWORD = "your_pass",\nMAIL_PORT = 587,\nMAIL_SERVER = "email_service",\nMAIL_TLS = True,\nMAIL_SSL = False)
         ''')

        self.settings = settings.dict()


    async def __aenter__(self): #setting up a connection
        await self._configure_connection()
        return self

    async def __aexit__(self, exc_type, exc, tb): #closing the connection
        await self.session.quit()


    async def _configure_connection(self):
        try:
            self.session = aiosmtplib.SMTP(
                hostname = self.settings.get("MAIL_SERVER"), 
                port = self.settings.get("MAIL_PORT"), 
                use_tls= self.settings.get("MAIL_SSL"),
                start_tls = self.settings.get("MAIL_TLS")
               )
            await self.session.connect()

            await self.session.login(
                self.settings.get("MAIL_USERNAME"), 
                self.settings.get("MAIL_PASSWORD")
                )
           
        except Exception as error:
            raise ConnectionErrors(f"Exception raised {error}, check your credentials or email service configuration") 
