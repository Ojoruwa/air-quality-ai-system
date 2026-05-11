import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Air Quality Cloud Dashboard")

st.title("🌍 Air Quality Cloud Intelligence System")

API_URL = "https://air-quality-ai-system.onrender.com"

# -----------------------------
# INPUTS
# -----------------------------
st.sidebar.header("Inputs")

data = {
    "PM10": st.sidebar.slider("PM10", 0, 300, 80),
    "PM2_5": st.sidebar.slider("PM2.5", 0, 200, 50),
    "NO2": st.sidebar.slider("NO2", 0, 150, 20),
    "SO2": st.sidebar.slider("SO2", 0, 100, 10),
    "O3": st.sidebar.slider("O3", 0, 200, 30),
    "Temperature": st.sidebar.slider("Temperature", 0, 50, 28),
    "Humidity": st.sidebar.slider("Humidity", 0, 100, 60),
    "WindSpeed": st.sidebar.slider("WindSpeed", 0, 50, 5)
}

# -----------------------------
# CALL API
# -----------------------------
if st.button("Predict via Cloud API 🚀"):

    response = requests.post(API_URL, json=data)

    result = response.json()

    st.subheader("Prediction Result")

    if result["prediction"] == 0:
        st.success("🟢 Low Risk")
    elif result["prediction"] == 1:
        st.warning("🟠 Medium Risk")
    else:
        st.error("🔴 High Risk")

    if result["probabilities"]:
        st.write("Probabilities:")
        st.bar_chart(pd.DataFrame(result["probabilities"]))