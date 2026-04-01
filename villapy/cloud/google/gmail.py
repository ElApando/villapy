""" DOC """

# pylint: disable=no-member

from typing import Dict, Any

import base64
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials # type: ignore
from googleapiclient.discovery import build # type: ignore

class Gmail:
    """ DOC """

    def __init__(self, di_routes: Dict[str, str], di_scope: Dict[str, Any]) -> None:
        """ DCO """

        self.creds = Credentials.from_authorized_user_file(di_routes["token"], di_scope["email"]) # type: ignore

    def send_email_gmail(self, st_to:str, st_subject:str, st_body:str): # Prueba uniatria 
        """ DOC """

        service = build("gmail", "v1", credentials = self.creds) # type: ignore

        message = MIMEText(st_body)
        message["to"] = st_to
        message["subject"] = st_subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        service.users().messages().send( # type: ignore
            userId="me",
            body={"raw": raw_message}
        ).execute()

# Finite Incantatem
