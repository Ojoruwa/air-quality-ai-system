from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel
import logging

from api.database import init_db, save_prediction

app = FastAPI()

# -----------------------------
# INIT SYSTEMS
# -----------------------------
logging.basicConfig(level=logging.INFO)
init_db()

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
# HEALTH CHECK
# -----------------------------
@app.get("/")
def home():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# -----------------------------
# PREDICT + LOG + STORE (MLOPS CORE)
# -----------------------------
@app.post("/predict")
def predict(data: InputData):

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

    prediction = int(model.predict(features)[0])
    probabilities = model.predict_proba(features)[0].tolist()

    # -----------------------------
    # LOGGING
    # -----------------------------
    logging.info(f"Input: {data.dict()}")
    logging.info(f"Prediction: {prediction}")

    # -----------------------------
    # SAVE TO DATABASE (MLOPS CORE)
    # -----------------------------
    save_prediction(data.dict(), prediction)

    return {
        "prediction": prediction,
        "probabilities": probabilities
    }