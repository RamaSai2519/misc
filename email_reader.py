import imaplib
import email
from email.message import Message
from email.header import decode_header
from typing import List, Dict, Any
from shared.db.base import Database


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


class EmailParser:
    @staticmethod
    def parse_email(msg: Message) -> Dict[str, Any]:
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        sender = msg.get("From")
        body = ""
        attachments = []
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_payload(decode=True) is not None:
                    try:
                        body += part.get_payload(decode=True).decode()
                    except UnicodeDecodeError:
                        try:
                            body += part.get_payload(
                                decode=True).decode('latin-1')
                        except UnicodeDecodeError:
                            body += "[Unable to decode content]"
                if part.get("Content-Disposition") is not None:
                    filename = part.get_filename()
                    if filename:
                        attachments.append(filename)
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except UnicodeDecodeError:
                try:
                    body = msg.get_payload(decode=True).decode('latin-1')
                except UnicodeDecodeError:
                    body = "[Unable to decode content]"
        return {"sender": sender, "subject": subject, "body": body, "attachments": attachments}


class EmailDatabase:
    def __init__(self, db_name: str = 'test', collection_name: str = 'emails') -> None:
        self.client = Database().client
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_email(self, email_data: Dict[str, Any]) -> None:
        self.collection.insert_one(email_data)

    def close(self) -> None:
        self.client.close()


def main() -> None:
    username = "ramasathyasai2006@gmail.com"
    password = "zzib hlno doly xeex"

    search_by = input(
        "Search by sender or subject? (sender(1)/subject(2)): ").strip().lower()
    search_value = input("Enter the search value: ").strip()

    if search_by == '1':
        search_criteria = f'FROM "{search_value}"'
    elif search_by == "2":
        search_criteria = f'SUBJECT "{search_value}*"'
    else:
        print("Invalid search criteria")
        return

    email_client = EmailClient(username, password)
    email_ids = email_client.search_emails(search_criteria)

    email_db = EmailDatabase()

    for email_id in email_ids:
        msg = email_client.fetch_email(email_id)
        email_data = EmailParser.parse_email(msg)
        email_db.insert_email(email_data)

    email_client.logout()
    email_db.close()


if __name__ == "__main__":
    main()
