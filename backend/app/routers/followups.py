from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db
from app.dependencies import get_active_user
from app.models import User

router = APIRouter(prefix="/followups", tags=["followups"])

@router.post("/", response_model=schemas.FollowUpOut)
def create_followup(followup: schemas.FollowUpCreate,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_active_user)):
    return crud.create_followup(db, followup, user.id)

@router.get("/", response_model=List[schemas.FollowUpOut])
def list_followups(db: Session = Depends(get_db),
                   user: User = Depends(get_active_user)):
    return crud.get_user_followups(db, user.id)

@router.delete("/{followup_id}", response_model=schemas.FollowUpOut)
def delete_followup(followup_id: int,
                    db: Session = Depends(get_db),
                    user: User = Depends(get_active_user)):
    deleted = crud.delete_followup(db, followup_id, user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return deleted
