from sqlalchemy import Column, Integer, String, DateTime, ARRAY, JSON
from database import Base


class Email(Base):
    __tablename__ = "email"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(50), unique=True)
    subject = Column(String(256))
    labels = Column(ARRAY(String))
    mime_type = Column(String(50))
    from_email = Column(String(100))
    to_email = Column(String(100))
    parts = Column(ARRAY(JSON))
    date = Column(DateTime)