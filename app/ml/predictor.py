import joblib
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.joblib")

model = joblib.load(model_path)

FEATURE_COLUMNS = [
    "fever","cough","fatigue","rash",
    "chest_pain","shortness_breath",
    "age_over_60","diabetes"
]

def predict_disease(input_dict: dict):
    df = pd.DataFrame([input_dict], columns=FEATURE_COLUMNS)

    prediction = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]

    # Get confidence for predicted class
    class_index = list(model.classes_).index(prediction)
    confidence = round(probabilities[class_index] * 100, 2)

    return prediction, confidence