from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class EventBase(BaseModel):
    title: str
    date: date
    time: time
    description: Optional[str] = None
    event_link: Optional[str] = None
    address: Optional[str] = None

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    class Config:
        orm_mode = True
