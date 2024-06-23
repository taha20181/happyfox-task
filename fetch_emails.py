from sqlalchemy import exc
from email.utils import parsedate_to_datetime

from database import SessionLocal
from utils import authenticate
from models import Email


def fetch_user_emails(service, message_count=1):
    results = service.users().messages().list(
        userId='me', labelIds=['INBOX'], maxResults=message_count).execute()

    messages = results.get('messages', [])

    response = []
    for message in messages:
        msg = service.users().messages().get(
            userId='me', id=message['id']).execute()
        
        headers = msg['payload']['headers']
        headers = {header['name'] : header['value'] for header in headers}

        response.append(
            {
                "message_id" : msg['id'],
                "labels" : msg['labelIds'],
                "mime_type" : msg['payload']['mimeType'],
                "parts" : msg['payload'].get('parts'),
                "subject" : headers['Subject'],
                "from_email" : headers['From'],
                "to_email" : headers['To'],
                "date" : parsedate_to_datetime(headers['Date'])
            }
        )

    return response


def insert_emails(records):
    i = 0
    for record in records:
        email = Email(
            message_id = record['message_id'],
            labels = record['labels'],
            mime_type = record['mime_type'],
            parts = record['parts'],
            subject = record['subject'],
            from_email = record['from_email'],
            to_email = record['to_email'],
            date = record['date']
        )

        try:
            session = SessionLocal()
            session.add(email)
            session.commit()
            session.refresh(email)
            i += 1
        except exc.IntegrityError as e:
            session.rollback()
        except Exception as e:
            session.rollback()
        finally:
            session.close()
    
    print(i, "records inserted")


if __name__ == '__main__':
    service = authenticate()
    data = fetch_user_emails(service, 10)
    print(len(data))
    insert_emails(data)