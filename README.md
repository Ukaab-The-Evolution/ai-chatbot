# Truck Driver Assistant Chatbot

This is a Streamlit-powered chatbot designed to assist truck drivers with practical advice.

```bash
pip install streamlit python-dotenv google-genai
```

### 1. Set Up Your API Key
Create a file named `chatbot.env` in the project directory with the following content:

```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

Replace `your_google_gemini_api_key_here` with your actual Gemini API key.

### 2. Run the Chatbot
Start the Streamlit app with:

```bash
streamlit run streamlit_chatbot.py
```

The chatbot will open in your browser.

## Troubleshooting
- If you see an error about the API key, make sure your `chatbot.env` file is present and contains the correct key.
- Ensure all required Python packages are installed.