from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    followups = relationship("FollowUp", back_populates="owner")

class FollowUp(Base):
    __tablename__ = "followups"
    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, nullable=False)
    subject = Column(String)
    notes = Column(String)
    date_sent = Column(DateTime, default=datetime.utcnow)
    follow_up_date = Column(DateTime)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="followups")