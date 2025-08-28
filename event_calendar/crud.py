from sqlalchemy.orm import Session
from . import models, schemas
import smtplib
from email.message import EmailMessage
from typing import Any
from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
RECIPIENT = os.getenv("RECEIVER_MAIL")

def send_email(event: Any) -> bool:
    if not EMAIL_USER or not EMAIL_PASS:
        print("EMAIL_USER or EMAIL_PASS not set in .env")
        return False

    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_USER
        msg["To"] = RECIPIENT   
        msg["Subject"] = f"Event Confirmation: {getattr(event, 'title', 'No Title')}"

        body = (
            f"✅ Event confirmed:\n\n"
            f"Title: {getattr(event, 'title', 'N/A')}\n"
            f"Date: {getattr(event, 'date', 'N/A')}\n"
            f"Time: {getattr(event, 'time', 'N/A')}\n"
            f"Description: {getattr(event, 'description', 'N/A')}\n"
        )
        msg.set_content(body)

        # Connect to Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        print(f"Email successfully sent to {RECIPIENT}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("Authentication failed. Check EMAIL_USER / EMAIL_PASS (use App Password for Gmail).")
    except Exception as e:
        print(f"Failed to send email: {e}")

    return False


def create_event(db: Session, event: schemas.EventCreate):
    try:
        db_event = models.Event(**event.dict())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        send_email(db_event)
        return db_event
    except Exception as e:
        print(f"Error creating event: {e}")
        db.rollback()
        return None


def get_events(db: Session):
    try:
        return db.query(models.Event).order_by(models.Event.date, models.Event.time).all()
    except Exception as e:
        print(f"Error fetching events: {e}")
        return []


def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    try:
        db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if db_event:
            for key, value in event.dict(exclude_unset=True).items():
                setattr(db_event, key, value)
            db.commit()
            db.refresh(db_event)
        return db_event
    except Exception as e:
        print(f"Error updating event: {e}")
        db.rollback()
        return None


def delete_event(db: Session, event_id: int):
    try:
        db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
        if db_event:
            db.delete(db_event)
            db.commit()
        return db_event
    except Exception as e:
        print(f"Error deleting event: {e}")
        db.rollback()
        return None
