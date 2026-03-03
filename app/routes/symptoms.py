from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import SymptomRequest
from app.services.diagnosis_service import diagnose, get_consultations
from app.database import get_db
from app.auth import get_current_doctor

router = APIRouter()


@router.post("/check-symptoms")
def check_symptoms(
    data: SymptomRequest,
    db: Session = Depends(get_db),
    current_doctor = Depends(get_current_doctor)
):

    symptoms = [s.lower() for s in data.symptoms]
    age = data.patient.age
    conditions = [c.lower() for c in data.patient.pre_existing_conditions]

    return diagnose(symptoms, age, conditions, db, current_doctor.id)


@router.get("/consultations")
def fetch_consultations(
    db: Session = Depends(get_db),
    current_doctor = Depends(get_current_doctor)
):

    return get_consultations(db, current_doctor.id)