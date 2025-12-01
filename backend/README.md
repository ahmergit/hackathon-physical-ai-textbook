# 🤖 Physical AI Textbook - Backend API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Agents_SDK-412991.svg)](https://openai.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-FF6B6B.svg)](https://qdrant.tech/)

> **Backend API for the Physical AI & Humanoid Robotics Interactive Textbook — featuring AI-powered chatbot with RAG, user authentication, and profile management.**

---

## ✨ Features

### 🤖 AI Chatbot
- **RAG Architecture** - Retrieval-Augmented Generation using textbook content
- **OpenAI GPT-4o** - Advanced language model for intelligent responses
- **OpenAI Agents SDK** - Agent orchestration for complex queries
- **Qdrant Vector Database** - Semantic search over textbook embeddings
- **Streaming Responses** - Real-time SSE streaming for chat

### 🔐 Authentication System
- **Email/Password Auth** - Secure registration with email verification
- **Google OAuth 2.0** - Single sign-on with Google accounts
- **JWT Tokens** - Secure session management with refresh tokens
- **Rate Limiting** - API protection against abuse

### 👤 User Profiles
- **Onboarding Flow** - Capture user experience and learning goals
- **Experience Levels** - Track robotics, programming, and AI/ML background
- **Personalization** - Customize content based on user profile

---

## 🏗️ Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Settings and configuration
│   ├── database.py          # SQLAlchemy async engine
│   ├── chatbot/             # AI chatbot with RAG
│   │   ├── agent.py         # OpenAI Agents SDK integration
│   │   ├── qdrant_client.py # Vector database client
│   │   └── prompts.py       # System prompts
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic validation schemas
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── oauth.py         # Google OAuth endpoints
│   │   ├── profile.py       # User profile endpoints
│   │   └── chat.py          # Chatbot endpoints
│   ├── services/            # Business logic layer
│   └── utils/               # Utility functions
├── alembic/                 # Database migrations
├── scripts/                 # Data ingestion scripts
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── build.sh                 # Render build script
└── runtime.txt              # Python version for deployment
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **uv** (recommended) or pip
- **PostgreSQL** (production) or SQLite (development)

### 1️⃣ Clone & Install

```bash
git clone https://github.com/ahmergit/physical-ai-textbook-backend.git
cd physical-ai-textbook-backend

# Create virtual environment
uv venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt
```

### 2️⃣ Environment Setup

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Database
DATABASE_URL=sqlite:///./physical_ai.db

# JWT Authentication
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI (for chatbot)
OPENAI_API_KEY=sk-your-openai-key

# Qdrant (vector database)
QDRANT_URL=https://your-qdrant-instance.cloud
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=physical-ai-textbook

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# CORS
CORS_ORIGINS=http://localhost:3000
```

### 3️⃣ Database Setup

```bash
# Run migrations
uv run alembic upgrade head
```

### 4️⃣ Start Server

```bash
uv run uvicorn src.main:app --reload --port 8000
```

### 5️⃣ Verify Installation

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login with credentials |
| POST | `/api/auth/logout` | Logout user |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/verify` | Verify email token |

### OAuth
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/google` | Initiate Google OAuth |
| GET | `/api/auth/google/callback` | OAuth callback |

### Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/profile` | Get user profile |
| POST | `/api/profile` | Create profile |
| PUT | `/api/profile` | Update profile |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message (SSE streaming) |
| GET | `/api/chat/health` | Chatbot health check |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| GET | `/` | API information |

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 🚢 Deployment (Render)

### Option 1: Blueprint Deploy

Click the button below to deploy to Render:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 2: Manual Deploy

1. Create a new **Web Service** on Render
2. Connect this repository
3. Configure:
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables (see `.env.example`)

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Framework** | FastAPI 0.115 |
| **Language** | Python 3.11+ |
| **ORM** | SQLAlchemy 2.0 |
| **Migrations** | Alembic |
| **Validation** | Pydantic 2.x |
| **AI Model** | OpenAI GPT-4o |
| **Agent SDK** | OpenAI Agents SDK |
| **Vector DB** | Qdrant Cloud |
| **Auth** | FastAPI-Users, JWT |
| **OAuth** | Google OAuth 2.0 |

---

## 📚 Related

- **Frontend**: [hackathon-physical-ai-textbook](https://github.com/ahmergit/hackathon-physical-ai-textbook)
- **Live Site**: [ahmergit.github.io/hackathon-physical-ai-textbook](https://ahmergit.github.io/hackathon-physical-ai-textbook/)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
