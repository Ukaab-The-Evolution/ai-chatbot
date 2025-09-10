"""
Streamlit frontend for the chatbot.
Run with: streamlit run streamlit_chatbot.py
This frontend sends ChatRequest payloads to the FastAPI backend at http://localhost:8000/chat/
If the backend is not running with a Gemini API key, the offline fallback will respond.
"""

import streamlit as st
import requests
import time
from datetime import datetime

BACKEND_URL = st.secrets.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot (Streamlit)")
st.write("A simple frontend that talks to the local FastAPI backend. If the backend has no Gemini API key, it will run an offline fallback.")

# Simple UI
with st.form("chat_form"):
    user_message = st.text_area("Your message", placeholder="Type a message or say hello...", height=120)
    language = st.selectbox("Language", options=["english","urdu","punjabi","balochi","saraiki","pushto"], index=0)
    submitted = st.form_submit_button("Send")

if submitted and user_message:
    payload = {
        "user_id": "local_user",
        "role": "user",
        "message": user_message,
        "context": {"language": language},
        "attachments": None,
        "location": None,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        with st.spinner("Contacting backend..."):
            resp = requests.post(f"{BACKEND_URL}/chat", json=payload, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            st.markdown("**Bot:**")
            st.write(data.get("response", "<no response>"))
        else:
            st.error(f"Backend returned status {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Failed to contact backend: {e}")

# Provide a helper to run health
if st.button("Check backend health"):
    try:
        r = requests.get(f"{BACKEND_URL}/health", timeout=5)
        st.write(r.json())
    except Exception as e:
        st.error(f"Health check failed: {e}")
