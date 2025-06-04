from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_followup(db: Session, followup: schemas.FollowUpCreate, user_id: int):
    db_followup = models.FollowUp(**followup.dict(), owner_id=user_id)
    db.add(db_followup)
    db.commit()
    db.refresh(db_followup)
    return db_followup

def get_user_followups(db: Session, user_id: int):
    return db.query(models.FollowUp).filter(models.FollowUp.owner_id == user_id).all()

def delete_followup(db: Session, followup_id: int, user_id: int):
    db_followup = db.query(models.FollowUp).filter(models.FollowUp.id == followup_id,
                                                   models.FollowUp.owner_id == user_id).first()
    if db_followup:
        db.delete(db_followup)
        db.commit()
    return db_followup