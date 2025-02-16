import email
import imaplib
from email.message import Message
from typing import List


class EmailClient:
    def __init__(self, username: str, password: str, server: str = "imap.gmail.com") -> None:
        self.username = username
        self.password = password
        self.server = server
        self.mail = imaplib.IMAP4_SSL(self.server)
        self.mail.login(self.username, self.password)

    def search_emails(self, search_criteria: str) -> List[bytes]:
        self.mail.select("inbox")
        status, messages = self.mail.search(None, search_criteria)
        return messages[0].split()

    def fetch_email(self, email_id: bytes) -> Message:
        status, msg_data = self.mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                return email.message_from_bytes(response_part[1])

    def logout(self) -> None:
        self.mail.logout()
