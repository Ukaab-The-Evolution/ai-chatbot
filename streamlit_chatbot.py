import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types


# Load environment variables from chatbot.env
load_dotenv("chatbot.env")
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("API Key not found. Please check your chatbot.env file.")

# Initialize Gemini
client = genai.Client(api_key=API_KEY)
model = "gemini-2.0-flash"

def generate_response(history):
    contents = []
    for role, msg in history:
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg)]
            )
        )


    # Add system instruction for truck driver assistant
    system_instruction = types.Content(
        role="system",
        parts=[types.Part(text="You are a helpful assistant for pakistani truck drivers. Offer practical advice, safety tips, and support for life on the road. Be friendly, concise, and knowledgeable about trucking, logistics, and travel. Don't talk too much and don't be too verbose. Answer in the language the user used in the last message.")]
    )

    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        response_mime_type="text/plain"
    )

    # Generate and stream response
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config,
    ):
        response_text += chunk.text or ""

    return response_text

# Streamlit App Setup

st.set_page_config("Truck Driver Assistant", page_icon="🚚")
st.title("🚚 Truck Driver Assistant")
st.markdown("Chat with your **Truck Driver Assistant** for tips, advice, and support on the road.")

# Session state to store chat history
if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, message) tuples

# User input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("You:", placeholder="Ask your Truck Driver Assistant anything...")
    submitted = st.form_submit_button("Send")


if submitted and user_input.strip():
    # Add user input to chat history
    st.session_state.history.append(("user", user_input))

    # Get response from Gemini
    with st.spinner("Your assistant is thinking..."):
        response = generate_response(st.session_state.history)
    st.session_state.history.append(("model", response))

# Display conversation

for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🚚 Assistant:** {msg}")

# Clear button
if st.button("🧹 Clear Chat"):
    st.session_state.history = []
