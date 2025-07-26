"""
Streamlit web interface for weather alerts.
"""
import asyncio
import streamlit as st
from client.client import get_weather_alerts

st.set_page_config(page_title="🌤 Weather Alerts", layout="centered")
st.title("Live Weather Alerts")
st.write("Get weather alerts from the US National Weather Service (weather.gov)")

state = st.text_input("Enter US State Code (e.g., CA, TX, NY):", value="CA")

async def fetch_alerts(state: str):
    """Fetch weather alerts for the given state."""
    try:
        return await get_weather_alerts(state)
    except Exception as e:
        return f"Error: {e}"

if st.button("Fetch Alerts"):
    with st.spinner("Fetching alerts..."):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            alerts = loop.run_until_complete(fetch_alerts(state.strip().upper()))
            st.text_area("Alerts", alerts, height=400)
        except Exception as e:
            st.error(f"Error: {e}")
