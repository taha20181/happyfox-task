import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


HOST = os.environ['DB_HOST']
PORT = os.environ['DB_PORT']
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']
NAME = os.environ['DB_NAME']

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


if __name__ == '__main__':
    from utils import query_db
    from models import Email
    Base.metadata.create_all(bind=engine)
    query_db(Email)