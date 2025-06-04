from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import schemas, crud, database, models

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.SessionLocal)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not crud.pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = jwt.encode({
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.SessionLocal)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user