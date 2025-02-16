from email.message import Message
from email.header import decode_header
from typing import Dict, Any


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
