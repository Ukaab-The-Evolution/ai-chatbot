from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google.generativeai import GenerativeModel, configure
import os

# Load environment variables
load_dotenv("chatbot.env")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in chatbot.env")

# Configure Gemini API
configure(api_key=GEMINI_API_KEY)
model = GenerativeModel("gemini-1.5-flash")  

# FastAPI app
app = FastAPI()

# CORS setup (for Streamlit connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only. Restrict in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        if not message:
            raise HTTPException(status_code=400, detail="⚠️ No message provided.")

        result = model.generate_content(message)
        return {"response": result.text}
    except Exception as e:
        print("❌ Error:", e)
        raise HTTPException(status_code=500, detail="⚠️ Failed to fetch AI response.")
