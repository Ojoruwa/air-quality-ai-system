import pandas as pd
import joblib
import os

from sklearn.ensemble import HistGradientBoostingClassifier

# Load dataset
df = pd.read_csv("data/air_quality.csv")

df.columns = df.columns.str.strip()

FEATURES = [
    "PM10", "PM2_5", "NO2", "SO2",
    "O3", "Temperature", "Humidity", "WindSpeed"
]

target = "HealthImpactClass"

X = df[FEATURES]
y = df[target]

# Train model
model = HistGradientBoostingClassifier(random_state=42)
model.fit(X, y)

# Create folder if not exists
os.makedirs("model", exist_ok=True)

# SAVE MODEL HERE (IMPORTANT)
joblib.dump(model, "model/model.pkl")

print("✔ Model saved successfully in model/model.pkl")