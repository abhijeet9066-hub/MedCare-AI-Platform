import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Synthetic dataset
data = [
    # fever, cough, fatigue, rash, chest_pain, shortness_breath, age_over_60, diabetes, target
    [1,1,1,0,0,0,0,0, "Flu"],
    [1,0,0,1,0,0,0,0, "Viral Infection"],
    [0,0,0,0,1,1,1,1, "Cardiac Issue"],
    [1,1,0,0,0,0,1,0, "Flu"],
    [1,0,1,1,0,0,0,0, "Viral Infection"],
    [0,0,0,0,1,1,0,1, "Cardiac Issue"],
]

columns = [
    "fever","cough","fatigue","rash",
    "chest_pain","shortness_breath",
    "age_over_60","diabetes","target"
]

df = pd.DataFrame(data, columns=columns)

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

print("Model Evaluation:")
print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "app/ml/model.joblib")

print("Model saved successfully.")