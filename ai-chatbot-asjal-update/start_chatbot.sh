#!/bin/bash
# Simple helper to run the backend (uvicorn) for development.
# Make sure to create a chatbot.env with GEMINI_API_KEY if you want Gemini functionality.
export $(grep -v '^#' chatbot.env 2>/dev/null | xargs) || true
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
