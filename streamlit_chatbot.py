import os
import requests
import streamlit as st
from dotenv import load_dotenv
import datetime
import re

# Load API key
load_dotenv("chatbot.env")
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ API Key not found. Please check chatbot.env file.")
    st.stop()

# Session states
if "email_verified" not in st.session_state:
    st.session_state.email_verified = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "history" not in st.session_state:
    st.session_state.history = []

MAX_HISTORY = 20

# Send message to backend
def send_message_to_backend(user_message):
    try:
        response = requests.post(
            "http://127.0.0.1:3000/chat",
            json={"message": user_message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("response", "⚠️ No response from AI.")
        else:
            return f"⚠️ API error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"⚠️ Could not connect to chatbot API: {e}"

# Streamlit UI
st.set_page_config("Truck Driver Assistant", page_icon="🚚")
st.title("🚚 Truck Driver Assistant")

# Email input
if not st.session_state.email_verified:
    email = st.text_input("📧 Enter your email to start:", placeholder="example@email.com")
    if st.button("✅ Proceed"):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.session_state.email_verified = True
            st.session_state.user_email = email
            st.success("✅ Email accepted! You can now chat with the assistant.")
            st.rerun()
        else:
            st.error("❌ Please enter a valid email address to continue.")
    st.stop()

# Quick Questions
st.subheader("🔹 Quick Questions")
cols = st.columns(3)
if cols[0].button("🚚 Best Routes"):
    st.session_state.history.append(("user", "What are the safest trucking routes in Pakistan?"))
if cols[1].button("🛠️ Truck Maintenance"):
    st.session_state.history.append(("user", "Give me some truck maintenance tips."))
if cols[2].button("⛽ Fuel Saving"):
    st.session_state.history.append(("user", "How can I save fuel on long trips?"))

# Chat Form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Ask your Truck Driver Assistant anything...")
    submitted = st.form_submit_button("Send")

if submitted and user_input.strip():
    timestamp = datetime.datetime.now().strftime("%H:%M")
    st.session_state.history.append(("user", f"{timestamp} - {user_input}"))

    with st.spinner("💡 Your assistant is thinking..."):
        bot_reply = send_message_to_backend(user_input)
        st.session_state.history.append(("model", f"{timestamp} - {bot_reply}"))

    if len(st.session_state.history) > MAX_HISTORY:
        st.session_state.history = st.session_state.history[-MAX_HISTORY:]

# Display conversation
for role, msg in st.session_state.history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(f"**{'🧑 You' if role == 'user' else '🚚 Assistant'}:** {msg}")

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.history = []
    st.rerun()

