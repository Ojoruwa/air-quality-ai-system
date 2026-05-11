import streamlit as st
import requests
import pandas as pd
import sqlite3

st.set_page_config(page_title="Air Quality MLOps Dashboard", layout="wide")

st.title("🌍 Air Quality MLOps System")

API_URL = "https://air-quality-ai-system.onrender.com/predict"

DB_PATH = "api/air_quality.db"

# -----------------------------
# FETCH HISTORY
# -----------------------------
def load_history():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM predictions ORDER BY id DESC", conn)
    conn.close()
    return df

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Inputs")

data = {
    "PM10": st.sidebar.slider("PM10", 0, 300, 80),
    "PM2_5": st.sidebar.slider("PM2.5", 0, 200, 50),
    "NO2": st.sidebar.slider("NO2", 0, 150, 20),
    "SO2": st.sidebar.slider("SO2", 0, 100, 10),
    "O3": st.sidebar.slider("O3", 0, 200, 30),
    "Temperature": st.sidebar.slider("Temp", 0, 50, 28),
    "Humidity": st.sidebar.slider("Humidity", 0, 100, 60),
    "WindSpeed": st.sidebar.slider("Wind", 0, 50, 5)
}

# -----------------------------
# PREDICT
# -----------------------------
if st.button("Predict"):

    response = requests.post(API_URL, json=data)
    result = response.json()

    st.write(result)

    if "prediction" in result:
        st.success(f"Prediction: {result['prediction']}")

# -----------------------------
# HISTORY DASHBOARD (MLOPS FEATURE)
# -----------------------------
st.subheader("📊 Prediction History")

try:
    history = load_history()
    st.dataframe(history)

    st.subheader("Prediction Distribution")
    st.bar_chart(history["prediction"].value_counts())

except Exception as e:
    st.warning("No history data yet or DB not found.")