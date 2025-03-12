from email_client import EmailClient
from email_parser import EmailParser
from email_database import EmailDatabase
from details_extractor import DetailsExtractor


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
        extractor = DetailsExtractor(email_data.get('body', ''))
        details = extractor.extract_details()
        email_db.insert_email(email_data)
    email_client.logout()
    email_db.close()


if __name__ == "__main__":
    main()
