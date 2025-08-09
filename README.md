# 🚚 Truck Driver Assistant – AI Chatbot

An AI-powered chatbot that helps truck drivers with information such as the best trucking routes, vehicle maintenance tips, and fuel-saving techniques. Built with **Streamlit** for the frontend and **Python + Gemini AI** for the backend.

---

## 📌 Features

- ✅ Email verification before starting the chat
- 💬 Natural language conversations powered by Gemini AI
- 🛣️ Quick access questions: routes, maintenance, fuel savings
- 🕓 Timestamped chat history
- 🧹 Option to clear chat
- 🔐 Environment-based API key handling

---

## 📁 Project Structure

```bash
📦 truck-driver-assistant
│
├── streamlit_chatbot.py       # Frontend: Streamlit app
├── server.py                  # Backend: Fastify server with Gemini API
├── chatbot.env                # Environment variables (Gemini API key)
├── start_chatbot.sh           # Bash script to run both frontend and backend
├── README.md                  # Project documentation (this file)
```

---

## 🔐 Environment Setup

1. Go to [Google MakerSuite](https://makersuite.google.com/)
2. Generate your **Gemini API Key**
3. Create a file named `chatbot.env` in the root directory with the following content:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

---

## 📦 Requirements

You need to install dependencies for **both the frontend (Python)** and **backend (Node.js)**.

### ✅ Python Requirements (Frontend)

Make sure Python 3.10+ is installed. Then run:

```bash
pip install streamlit requests python-dotenv
```

These libraries handle the chat UI, API communication, and environment variables.


## 🚀 How to Run the Project

You can either run it **automatically using the provided script**, or start each part manually.

### 🔁 Option 1: Run Everything (Recommended)

The `start_chatbot.sh` script:
- Kills any process using port 3000
- Starts the backend server
- Launches the Streamlit frontend

---

🧩 Option 2: Manual Execution
1. Start the FastAPI Backend
```bash
uvicorn server:app --host 127.0.0.1 --port 3000
```
2. Start the Streamlit Frontend (in a new terminal)
```bash
streamlit run streamlit_chatbot.py
```

Then open your browser and go to:
```bash
👉 http://localhost:8501
```
This launches the Fastify API server at `http://localhost:3000`.


## ⚙️ How It Works

- **Frontend (`streamlit_chatbot.py`)** handles user input, email verification, chat history, and UI.
- **Backend (`server.js`)** receives the message and uses Gemini AI to generate responses.
- Communication happens via an internal API call to `http://localhost:3000/chat`.
