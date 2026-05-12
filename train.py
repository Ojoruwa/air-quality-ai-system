import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/air_quality.csv")

# -----------------------------
# CLEAN FEATURES (AUTO ALIGNMENT)
# -----------------------------
features = [
    "PM10", "PM2_5", "NO2", "SO2",
    "O3", "Temperature", "Humidity", "WindSpeed"
]

X = df[features]
y = df["HealthImpactClass"]

# -----------------------------
# TRAIN TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# SCALING (IMPORTANT)
# -----------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -----------------------------
# MULTIPLE MODELS (COMPARISON)
# -----------------------------
models = {
    "logreg": LogisticRegression(max_iter=1000),
    "rf": RandomForestClassifier(n_estimators=200),
    "gb": GradientBoostingClassifier()
}

best_model = None
best_score = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)

    print(f"{name} accuracy: {score}")

    if score > best_score:
        best_score = score
        best_model = model

# -----------------------------
# FINAL MODEL REPORT
# -----------------------------
y_pred = best_model.predict(X_test)
print(classification_report(y_test, y_pred))

# -----------------------------
# SAVE EVERYTHING (CRITICAL FIX)
# -----------------------------
package = {
    "model": best_model,
    "scaler": scaler,
    "features": features
}

joblib.dump(package, "api/model.pkl")

print("Model saved successfully")