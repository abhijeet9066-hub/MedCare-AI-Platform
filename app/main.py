from fastapi import FastAPI
from app.routes.symptoms import router as symptoms_router
from app.routes.auth import router as auth_router
from app.database import engine
from app.models_db import Base

app = FastAPI(title="MedCare AI Platform")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(symptoms_router)