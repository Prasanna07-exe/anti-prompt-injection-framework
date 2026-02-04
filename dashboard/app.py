# dashboard/app.py

import streamlit as st
import requests

st.set_page_config(page_title="Prompt Injection Dashboard")

st.title("🛡️ Anti Prompt Injection Monitoring Dashboard")

BACKEND_URL = "http://127.0.0.1:8000/metrics"

try:
    response = requests.get(BACKEND_URL)
    metrics = response.json()
except Exception:
    st.error("Backend not running. Please start FastAPI server.")
    st.stop()

st.metric("Total Prompts", metrics["total_prompts"])
st.metric("Blocked Attacks", metrics["blocked"])
st.metric("Sanitized Prompts", metrics["sanitized"])
st.metric("Allowed Prompts", metrics["allowed"])

st.bar_chart({
    "Blocked": metrics["blocked"],
    "Sanitized": metrics["sanitized"],
    "Allowed": metrics["allowed"]
})
