from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    consultations = relationship("Consultation", back_populates="doctor")


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(String)
    predicted_condition = Column(String)
    severity_score = Column(Integer)
    risk_level = Column(String)
    ml_confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    doctor_id = Column(Integer, ForeignKey("doctors.id"))

    doctor = relationship("Doctor", back_populates="consultations")