from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import get_current_user
from app.models import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_active_user(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user