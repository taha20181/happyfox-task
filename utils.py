from sqlalchemy import exc
import os.path
from database import SessionLocal

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
creds = None

def authenticate():
    global creds
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    return service


def query_db(table):
    try:
        session = SessionLocal()
        records = session.query(table).all()
        print("total records : ", len(records))
        return records
    except exc.IntegrityError as e:
        session.rollback()
    except Exception as e:
        session.rollback()
    finally:
        session.close()