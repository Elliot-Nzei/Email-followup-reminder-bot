from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class FollowUpBase(BaseModel):
    recipient: EmailStr
    subject: Optional[str]
    notes: Optional[str]
    follow_up_date: datetime

class FollowUpCreate(FollowUpBase): pass

class FollowUpOut(FollowUpBase):
    id: int
    date_sent: datetime
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str