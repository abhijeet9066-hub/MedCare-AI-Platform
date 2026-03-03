from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models_db import Doctor
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    existing = db.query(Doctor).filter(Doctor.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(data.password)

    doctor = Doctor(email=data.email, password=hashed_pw)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {"message": "Doctor registered successfully"}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    doctor = db.query(Doctor).filter(Doctor.email == data.email).first()
    if not doctor or not verify_password(data.password, doctor.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": doctor.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }