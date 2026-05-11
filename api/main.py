from fastapi import FastAPI
import joblib
import numpy as np
import os

app = FastAPI(title="Air Quality Health API")

# -----------------------------
# SAFE MODEL PATH
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

# Load model
model = joblib.load(MODEL_PATH)

# -----------------------------
# FEATURES
# -----------------------------
FEATURES = [
    "PM10",
    "PM2_5",
    "NO2",
    "SO2",
    "O3",
    "Temperature",
    "Humidity",
    "WindSpeed"
]

# -----------------------------
# API ROUTE
# -----------------------------
@app.post("/predict")
def predict(data: dict):

    input_data = np.array([[data[f] for f in FEATURES]])

    prediction = model.predict(input_data)[0]

    probabilities = None

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_data)[0].tolist()

    return {
        "prediction": int(prediction),
        "probabilities": probabilities
    }