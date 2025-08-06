#!/bin/bash

echo "🚀 Starting AI Chatbot..."

cd "$(dirname "$0")"

# Kill any existing processes
echo "🔧 Cleaning old processes..."
lsof -ti:3000 | xargs kill -9 2>/dev/null
pkill -f streamlit 2>/dev/null

# Start FastAPI
echo "🧠 Starting FastAPI backend..."
nohup uvicorn server:app --host 127.0.0.1 --port 3000 > backend.log 2>&1 &

sleep 3  # give time for backend to boot

# Start Streamlit
echo "💬 Launching Streamlit frontend..."
streamlit run streamlit_chatbot.py
