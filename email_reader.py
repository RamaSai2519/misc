import imaplib
import email
from shared.db.base import Database
from email.header import decode_header

# MongoDB setup
client = Database().client
db = client['test']
collection = db['emails']

# Email credentials
username = "ramasathyasai2006@gmail.com"
password = "zzib hlno doly xeex"

# Search criteria
search_by = input(
    "Search by sender or subject? (sender(1)/subject(2)): ").strip().lower()
search_value = input("Enter the search value: ").strip()

if search_by == '1':
    search_criteria = f'FROM "{search_value}"'
elif search_by == "2":
    search_criteria = f'SUBJECT "{search_value}*"'
else:
    print("Invalid search criteria")
    exit()

# Connect to the Gmail server
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)
mail.select("inbox")

status, messages = mail.search(None, search_criteria)

email_ids = messages[0].split()

for email_id in email_ids:
    status, msg_data = mail.fetch(email_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
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

            collection.insert_one({
                "sender": sender,
                "subject": subject,
                "body": body,
                "attachments": attachments
            })

# Close the connection
mail.logout()
client.close()
