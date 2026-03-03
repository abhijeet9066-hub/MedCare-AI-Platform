from pydantic import BaseModel
from typing import List, Optional


class PatientProfile(BaseModel):
    age: int
    weight: float
    pre_existing_conditions: Optional[List[str]] = []


class SymptomRequest(BaseModel):
    symptoms: List[str]
    patient: PatientProfile