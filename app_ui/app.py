import streamlit as st
import requests
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Air Quality Intelligence Dashboard",
    layout="wide"
)

st.title("🌍 Air Quality Intelligence Dashboard")
st.caption("Production AI System (Stable Version)")

# -----------------------------
# API
# -----------------------------
API_URL = "https://air-quality-ai-system.onrender.com/predict"

# -----------------------------
# SAFE API CALL FUNCTION
# -----------------------------
def safe_api_call(data):
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# -----------------------------
# INPUTS
# -----------------------------
st.sidebar.header("Environmental Inputs")

PM10 = st.sidebar.slider("PM10", 0, 300, 80)
PM2_5 = st.sidebar.slider("PM2.5", 0, 200, 50)
NO2 = st.sidebar.slider("NO2", 0, 150, 20)
SO2 = st.sidebar.slider("SO2", 0, 100, 10)
O3 = st.sidebar.slider("O3", 0, 200, 30)
Temperature = st.sidebar.slider("Temperature", 0, 50, 28)
Humidity = st.sidebar.slider("Humidity", 0, 100, 60)
WindSpeed = st.sidebar.slider("WindSpeed", 0, 50, 5)

# -----------------------------
# MAIN BUTTON
# -----------------------------
if st.button("🚀 Predict Air Quality Risk"):

    data = {
        "PM10": PM10,
        "PM2_5": PM2_5,
        "NO2": NO2,
        "SO2": SO2,
        "O3": O3,
        "Temperature": Temperature,
        "Humidity": Humidity,
        "WindSpeed": WindSpeed
    }

    result = safe_api_call(data)

    st.subheader("📡 API Response")
    st.write(result)

    # -----------------------------
    # SAFE DISPLAY
    # -----------------------------
    if result and "prediction" in result:

        st.subheader("🧠 Prediction Result")

        if result["prediction"] == 0:
            st.success("🟢 Low Risk")
        elif result["prediction"] == 1:
            st.warning("🟠 Medium Risk")
        else:
            st.error("🔴 High Risk")

        if "probabilities" in result:
            st.subheader("📊 Probabilities")

            df = pd.DataFrame(
                [result["probabilities"]],
                columns=["Class 0", "Class 1", "Class 2"]
            )

            st.bar_chart(df)

    else:
        st.error("⚠️ API unavailable or invalid response")