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
st.caption("AI-powered air quality risk prediction system (Cloud Edition)")

# -----------------------------
# API CONNECTION (RENDER BACKEND)
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
Temperature = st.sidebar.slider("Temperature (°C)", 0, 50, 28)
Humidity = st.sidebar.slider("Humidity (%)", 0, 100, 60)
WindSpeed = st.sidebar.slider("Wind Speed", 0, 50, 5)

# -----------------------------
# MAIN ACTION
# -----------------------------
if st.button("🚀 Predict Air Quality Risk"):

    # Prepare data for API
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

    try:
        # Call backend API
        response = requests.post(API_URL, json=data, timeout=10)
        result = response.json()

        st.subheader("📡 API Response")
        st.write(result)

        # -----------------------------
        # SAFE PREDICTION HANDLING
        # -----------------------------
        if result and isinstance(result, dict) and "prediction" in result:

            st.subheader("🧠 Prediction Result")

            if result["prediction"] == 0:
                st.success("🟢 Low Risk Air Quality")
            elif result["prediction"] == 1:
                st.warning("🟠 Medium Risk Air Quality")
            else:
                st.error("🔴 High Risk Air Quality")

            # -----------------------------
            # PROBABILITIES (if available)
            # -----------------------------
            if "probabilities" in result and result["probabilities"]:

                st.subheader("📊 Prediction Probabilities")

                prob_df = pd.DataFrame(
                    [result["probabilities"]],
                    columns=["Class 0", "Class 1", "Class 2"]
                )

                st.bar_chart(prob_df)

        else:
            st.error("⚠️ Invalid response from API. Check backend deployment.")

    except Exception as e:
        st.error(f"❌ API request failed: {e}")