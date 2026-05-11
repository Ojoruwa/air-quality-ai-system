from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel
import logging

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI()

# -----------------------------
# LOGGING (PRODUCTION FEATURE)
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# LOAD MODEL
# -----------------------------
model = joblib.load("api/model.pkl")

# -----------------------------
# INPUT SCHEMA
# -----------------------------
class InputData(BaseModel):
    PM10: float
    PM2_5: float
    NO2: float
    SO2: float
    O3: float
    Temperature: float
    Humidity: float
    WindSpeed: float

# -----------------------------
# HEALTH CHECK (PRODUCTION)
# -----------------------------
@app.get("/")
def home():
    return {"status": "API running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# -----------------------------
# PREDICT ENDPOINT
# -----------------------------
@app.post("/predict")
def predict(data: InputData):

    # Convert input to model format
    features = np.array([[
        data.PM10,
        data.PM2_5,
        data.NO2,
        data.SO2,
        data.O3,
        data.Temperature,
        data.Humidity,
        data.WindSpeed
    ]])

    # Prediction
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0].tolist()

    # -----------------------------
    # LOGGING (PRODUCTION MONITORING)
    # -----------------------------
    logging.info(f"Input: {data.dict()}")
    logging.info(f"Prediction: {prediction}")

    return {
        "prediction": int(prediction),
        "probabilities": probabilities
    }