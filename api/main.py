from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel
import logging

from api.database import init_db, save_prediction

# -----------------------------
# FASTAPI INIT
# -----------------------------
app = FastAPI()

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(level=logging.INFO)

# -----------------------------
# INIT DATABASE
# -----------------------------
init_db()

# -----------------------------
# LOAD TRAINED PACKAGE
# -----------------------------
package = joblib.load("api/model.pkl")

model = package["model"]
scaler = package["scaler"]
features_list = package["features"]

# -----------------------------
# INPUT VALIDATION
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
# HOME ROUTE
# -----------------------------
@app.get("/")
def home():
    return {
        "status": "Air Quality API Running"
    }

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# -----------------------------
# PREDICTION ROUTE
# -----------------------------
@app.post("/predict")
def predict(data: InputData):

    try:

        # -----------------------------
        # INPUT → ARRAY
        # -----------------------------
        input_data = np.array([[
            data.PM10,
            data.PM2_5,
            data.NO2,
            data.SO2,
            data.O3,
            data.Temperature,
            data.Humidity,
            data.WindSpeed
        ]])

        # -----------------------------
        # APPLY SCALING
        # -----------------------------
        scaled_data = scaler.transform(input_data)

        # -----------------------------
        # PREDICTION
        # -----------------------------
        prediction = int(model.predict(scaled_data)[0])

        # -----------------------------
        # PROBABILITIES
        # -----------------------------
        probabilities = model.predict_proba(
            scaled_data
        )[0].tolist()

        # -----------------------------
        # SAVE TO DATABASE
        # -----------------------------
        save_prediction(data.dict(), prediction)

        # -----------------------------
        # LOGGING
        # -----------------------------
        logging.info(f"Input: {data.dict()}")
        logging.info(f"Prediction: {prediction}")

        # -----------------------------
        # RESPONSE
        # -----------------------------
        return {
            "prediction": prediction,
            "probabilities": probabilities,
            "model_features": features_list
        }

    except Exception as e:

        logging.error(str(e))

        return {
            "error": str(e)
        }