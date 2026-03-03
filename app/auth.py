import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import get_db
from app.models_db import Doctor

# 🔐 Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# 🔒 Password hashing config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔑 OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ==========================
# Password Utilities
# ==========================

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# ==========================
# JWT Token Creation
# ==========================

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ==========================
# Get Current Logged-In Doctor
# ==========================

def get_current_doctor(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        doctor_id = payload.get("sub")

        if doctor_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()

    if doctor is None:
        raise credentials_exception

    return doctor