from sqlalchemy.orm import Session
from app.ml.predictor import predict_disease
from app.models_db import Consultation


# Symptom weight system
SYMPTOM_WEIGHTS = {
    "fever": 2,
    "cough": 2,
    "fatigue": 1,
    "rash": 3,
    "headache": 1,
    "chest pain": 5,
    "shortness of breath": 4
}


def calculate_severity(symptoms, age, conditions):
    severity_score = 0

    for symptom in symptoms:
        severity_score += SYMPTOM_WEIGHTS.get(symptom, 0)

    if age > 60:
        severity_score += 2

    if "diabetes" in conditions or "hypertension" in conditions:
        severity_score += 2

    return severity_score


def categorize_risk(severity_score):
    if severity_score >= 8:
        return "High"
    elif severity_score >= 4:
        return "Moderate"
    return "Low"


def build_feature_vector(symptoms, age, conditions):
    return {
        "fever": 1 if "fever" in symptoms else 0,
        "cough": 1 if "cough" in symptoms else 0,
        "fatigue": 1 if "fatigue" in symptoms else 0,
        "rash": 1 if "rash" in symptoms else 0,
        "chest_pain": 1 if "chest pain" in symptoms else 0,
        "shortness_breath": 1 if "shortness of breath" in symptoms else 0,
        "age_over_60": 1 if age > 60 else 0,
        "diabetes": 1 if "diabetes" in conditions else 0
    }


def diagnose(symptoms, age, conditions, db: Session, doctor_id: int):

    severity_score = calculate_severity(symptoms, age, conditions)
    risk_level = categorize_risk(severity_score)

    feature_vector = build_feature_vector(symptoms, age, conditions)
    predicted_disease, ml_confidence = predict_disease(feature_vector)

    probability = min(severity_score * 8, 95)

    consultation = Consultation(
        symptoms=", ".join(symptoms),
        predicted_condition=predicted_disease,
        severity_score=severity_score,
        risk_level=risk_level,
        ml_confidence=ml_confidence,
        doctor_id=doctor_id
    )

    db.add(consultation)
    db.commit()

    return {
        "predicted_condition": predicted_disease,
        "ml_confidence_percent": ml_confidence,
        "severity_score": severity_score,
        "risk_level": risk_level,
        "probability_percent": probability,
        "recommendation":
            "Seek immediate medical attention"
            if risk_level == "High"
            else "Consult doctor if symptoms persist"
    }


def get_consultations(db: Session, doctor_id: int):

    consultations = (
        db.query(Consultation)
        .filter(Consultation.doctor_id == doctor_id)
        .order_by(Consultation.created_at.desc())
        .all()
    )

    return [
        {
            "id": c.id,
            "symptoms": c.symptoms,
            "predicted_condition": c.predicted_condition,
            "severity_score": c.severity_score,
            "risk_level": c.risk_level,
            "ml_confidence_percent": c.ml_confidence,
            "created_at": c.created_at
        }
        for c in consultations
    ]