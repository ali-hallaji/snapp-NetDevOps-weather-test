from jose import JWTError, jwt
from typing import Optional, Any
from datetime import timedelta, datetime, timezone

from fastapi.security.http import HTTPBasicCredentials
from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import settings
from model import SessionLocal, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PATH}/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(username: str):
    users = [
       User(username=settings.ROOT_USER, password=settings.ROOT_PASS)
   ]
    for user in users:
        if user.username == username:
            return user
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=[settings.ALGORITHM])
        if payload and payload.get('sub') == settings.ROOT_USER:
            return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
   