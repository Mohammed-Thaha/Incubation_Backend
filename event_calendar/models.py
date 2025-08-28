from sqlalchemy import Column, Integer, String, Date, Time, Text
from .database import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    description = Column(Text, nullable=True)
    event_link = Column(String, nullable=True)
    address = Column(String, nullable=True)
