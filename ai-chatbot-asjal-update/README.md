# 🚚 Truck Driver Assistant 

A production-ready FastAPI backend for a multi-language truck driver assistant chatbot with Google Gemini AI integration. Built following SOLID principles with clean architecture.

## 🏗️ Architecture Overview

This project implements a clean, modular architecture following SOLID principles:

```
truck-driver-assistant/
├── app/                    # Main application package
│   ├── __init__.py
│   ├── main.py            # FastAPI app factory
│   ├── api/               # API layer
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── chat.py    # Chat endpoints
│   │       └── utils.py   # Utility endpoints
│   ├── core/              # Core configuration
│   │   ├── __init__.py
│   │   └── config.py      # Settings & language config
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── schemas.py     # Pydantic models
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   ├── interfaces.py  # Service abstractions
│   │   ├── gemini_service.py  # AI service implementation
│   │   └── language_service.py # Language operations
│   └── utils/             # Utilities
│       ├── __init__.py
│       ├── exceptions.py  # Error handling
│       └── logging.py     # Logging configuration
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── railway.toml         # Railway deployment config
├── Procfile            # Process file for deployment
└── README.md           # This file
```

## ✨ Features

- 🌍 **Multi-language Support**: English, Urdu, Punjabi, Balochi, Saraiki, Pushto
- 🤖 **Google Gemini AI Integration**: Advanced AI responses for truck drivers
- 🔄 **Auto-routing**: Intelligent language detection and routing
- 📱 **RESTful API**: Clean, documented REST endpoints
- 🛡️ **Error Handling**: Comprehensive error management
- 📚 **Documentation**: Auto-generated API docs with Swagger
- 🚀 **Production Ready**: Railway deployment configuration
- 🔒 **CORS Support**: Frontend integration ready
- 📊 **Logging**: Structured logging for monitoring

## 🎯 SOLID Principles Implementation

### Single Responsibility Principle (SRP)
- Each module has one clear purpose
- Services handle specific business logic
- Routes only manage HTTP requests

### Open/Closed Principle (OCP)
- Easy to extend with new languages
- Can add new AI services without modification
- Extensible route structure

### Liskov Substitution Principle (LSP)
- All services implement interfaces
- Mock services for testing
- Interchangeable implementations

### Interface Segregation Principle (ISP)
- Small, focused interfaces
- No unnecessary dependencies
- Clean contracts

### Dependency Inversion Principle (DIP)
- Depends on abstractions, not concretions
- Dependency injection throughout
- Easy testing and mocking

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API key

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd truck-driver-assistant
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
# Copy environment template
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Edit chatbot.env and add your Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Run the application:**
```bash
python main.py
```

6. **Access the API:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

## 📚 API Documentation

### Authentication
No authentication required for this version.

### Base URL
- Local: `http://localhost:8000`
- Production: `https://your-railway-app.railway.app`

### Endpoints

#### Chat Endpoints

**Auto-route Chat**
```http
POST /chat
```
Automatically routes to appropriate language based on context.

**Language-specific Endpoints**
```http
POST /chat/english
POST /chat/urdu
POST /chat/punjabi
POST /chat/balochi
POST /chat/saraiki
POST /chat/pushto
```

#### Utility Endpoints

**Health Check**
```http
GET /health
```

**Supported Languages**
```http
GET /languages
```

### Request Schema

```json
{
  "user_id": "string",
  "role": "string",
  "message": "string",
  "context": {
    "screen": "string",
    "entity_id": "string",
    "language": "string"
  },
  "attachments": [
    {
      "type": "pdf|image",
      "url": "string",
      "filename": "string"
    }
  ],
  "location": {
    "latitude": 0.0,
    "longitude": 0.0
  },
  "timestamp": "2025-08-09T10:30:00Z"
}
```

### Response Schema

```json
{
  "response": "string",
  "language": "string",
  "timestamp": "2025-08-09T10:30:00Z",
  "user_id": "string"
}
```

### Example Request

```bash
curl -X POST "http://localhost:8000/chat/english" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "driver_123",
    "role": "user",
    "message": "What are some safety tips for driving in rain?",
    "context": {
      "screen": "safety_screen",
      "language": "english"
    },
    "timestamp": "2025-08-09T10:30:00Z"
  }'
```

### Example Response

```json
{
  "response": "Here are essential safety tips for driving in rain: 1) Reduce speed and increase following distance, 2) Turn on headlights for better visibility, 3) Avoid sudden braking or steering, 4) Check tire tread regularly, 5) If visibility is poor, pull over safely.",
  "language": "english",
  "timestamp": "2025-08-09T10:30:05Z",
  "user_id": "driver_123"
}
```


## 🚀 Deployment

### Railway Deployment

1. **Connect to Railway:**
   - Sign up at [railway.app](https://railway.app)
   - Connect your GitHub repository

2. **Environment Variables:**
   Set in Railway dashboard:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Deploy:**
   - Push to main branch
   - Railway automatically deploys using `railway.toml` configuration

### Manual Deployment

1. **Build and run:**
```bash
# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. **Using Docker (optional):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | - | Yes |
| `PORT` | Server port | 8000 | No |
| `HOST` | Server host | 0.0.0.0 | No |
| `DEBUG` | Debug mode | false | No |
| `CORS_ORIGINS` | Allowed CORS origins | * | No |

### Language Configuration

Supported languages and their codes:
- `english` - English
- `urdu` - اردو
- `punjabi` - ਪੰਜਾਬੀ
- `balochi` - بلوچی
- `saraiki` - سرائیکی
- `pushto` - پښتو

## 🐛 Troubleshooting

### Common Issues

**Import Errors**
- Ensure you're in the project root directory
- Check virtual environment is activated
- Verify all dependencies are installed

**API Key Issues**
- Verify `GEMINI_API_KEY` is set correctly
- Check API key has proper permissions
- Ensure `.env` file is named `chatbot.env`

**Port Issues**
- Default port is 8000
- Change with `PORT` environment variable
- Ensure port is not in use

**CORS Issues**
- Configure `CORS_ORIGINS` for production
- Use specific origins instead of `*`

### Development Guidelines

- Follow SOLID principles
- Write tests for new features
- Update documentation
- Use type hints
- Follow PEP 8 style guide

## Notes added by assistant
- Rewrote `app/core/config.py` and made `app/services/gemini_service.py` robust to missing Google Gemini client or API key (offline fallback available).
- Added `streamlit_chatbot.py` Streamlit frontend and `app/utils/speech_utils.py` as optional utilities.
- Added `start_chatbot.sh` for local development.
