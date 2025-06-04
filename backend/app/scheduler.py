from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models import FollowUp
from app.email_utils import send_email

def check_due_followups():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        due = db.query(FollowUp).filter(FollowUp.follow_up_date <= now).all()
        for item in due:
            send_email(item.recipient, item.subject or "Follow-Up Reminder", item.notes or "")
    finally:
        db.close()