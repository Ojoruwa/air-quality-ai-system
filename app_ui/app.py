import streamlit as st
import requests
import pandas as pd
import math

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Air Quality Intelligence Dashboard",
    layout="wide"
)

st.title("🌍 Air Quality Intelligence Dashboard")
st.caption("AI-powered environmental risk system (Production UI Upgrade)")

# -----------------------------
# API
# -----------------------------
API_URL = "https://air-quality-ai-system.onrender.com/predict"

# -----------------------------
# SIDEBAR INPUTS
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
# WHAT-IF SCORE (simple internal AQ index)
# -----------------------------
def compute_aqi(pm10, pm25, no2, so2, o3):
    return (0.4*pm10 + 0.3*pm25 + 0.1*no2 + 0.1*so2 + 0.1*o3)

aqi_value = compute_aqi(PM10, PM2_5, NO2, SO2, O3)

# -----------------------------
# GAUGE METER (TEXT VISUAL)
# -----------------------------
def show_gauge(value):
    level = ""
    color = ""

    if value < 50:
        level = "Good"
        color = "🟢"
    elif value < 100:
        level = "Moderate"
        color = "🟡"
    elif value < 150:
        level = "Unhealthy"
        color = "🟠"
    else:
        level = "Hazardous"
        color = "🔴"

    st.subheader("🎯 AQI Gauge Meter")
    st.markdown(f"### {color} {level}")
    st.progress(min(int(value), 300) / 300)

# -----------------------------
# FEATURE INSIGHT (NO SHAP)
# -----------------------------
def feature_insight(data):
    st.subheader("🧠 Pollution Drivers")

    impact = {
        "PM10": data["PM10"] * 0.4,
        "PM2.5": data["PM2_5"] * 0.3,
        "NO2": data["NO2"] * 0.1,
        "SO2": data["SO2"] * 0.1,
        "O3": data["O3"] * 0.1
    }

    df = pd.DataFrame(list(impact.items()), columns=["Feature", "Impact"])
    st.bar_chart(df.set_index("Feature"))

# -----------------------------
# MAIN
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

    # -----------------------------
    # AQI GAUGE
    # -----------------------------
    show_gauge(aqi_value)

    # -----------------------------
    # FEATURE INSIGHT
    # -----------------------------
    feature_insight(data)

    # -----------------------------
    # API CALL
    # -----------------------------
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        result = response.json()

        st.subheader("📡 Model Prediction")

        st.write(result)

        if result and "prediction" in result:

            if result["prediction"] == 0:
                st.success("🟢 Low Risk")
            elif result["prediction"] == 1:
                st.warning("🟠 Medium Risk")
            else:
                st.error("🔴 High Risk")

        else:
            st.error("Invalid API response")

    except Exception as e:
        st.error(f"API error: {e}")