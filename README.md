# 🤖 Physical AI & Humanoid Robotics Textbook

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Docusaurus](https://img.shields.io/badge/Docusaurus-3.9-green.svg)](https://docusaurus.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)](https://www.typescriptlang.org/)

> **An interactive online textbook exploring the frontier where artificial intelligence meets physical embodiment — from fundamentals to advanced applications.**

![Physical AI Textbook](book-source/static/img/book-cover.png)

---

## 📚 About This Project

This project is a comprehensive educational platform that teaches Physical AI and Humanoid Robotics concepts through an interactive online textbook. It features:

- **📖 3 Complete Chapters** covering Physical AI fundamentals, workforce transformation, and humanoid robotics
- **🤖 AI-Powered Chatbot** that answers questions based on textbook content using RAG (Retrieval-Augmented Generation)
- **🔐 User Authentication** with email/password and Google OAuth via Better Auth
- **📱 Responsive Design** optimized for desktop and mobile devices
- **🎨 Dark Theme** modern UI with excellent readability

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Docusaurus    │────▶│   Better Auth   │────▶│  Neon PostgreSQL │
│   Frontend      │     │   (Port 3001)   │     │    (Cloud DB)    │
│   (Port 3000)   │     └────────┬────────┘     └──────────────────┘
│                 │              │ JWT                    ▲
│                 │              ▼                        │
│                 │────▶┌─────────────────┐              │
│                 │     │    FastAPI      │──────────────┘
│                 │     │   (Port 8000)   │
└─────────────────┘     └─────────────────┘
```

### Services

| Service | Port | Description |
|---------|------|-------------|
| **Docusaurus** | 3000 | Frontend - Interactive textbook UI |
| **Better Auth** | 3001 | Authentication service (TypeScript) |
| **FastAPI** | 8000 | Backend API - Chatbot, profiles, user management |

---

## 📁 Project Structure

```
physical-ai-humaniod-robotics/
├── 📁 backend/                 # Backend services
│   ├── auth-ts/               # Better Auth service (TypeScript)
│   │   └── src/
│   │       ├── auth.ts        # Auth configuration
│   │       └── routes/        # Sync user endpoint
│   ├── src/                   # FastAPI application
│   │   ├── routers/           # API endpoints (chat, profile, user)
│   │   ├── models/            # SQLAlchemy models
│   │   ├── middleware/        # JWT authentication
│   │   └── services/          # Business logic
│   ├── alembic/               # Database migrations
│   └── tests/                 # Backend tests
│
├── 📁 book-source/            # Docusaurus frontend
│   ├── docs/                  # Textbook content (MDX)
│   │   ├── chapter-01/        # The Rise of Physical AI
│   │   ├── chapter-02/        # Humans, Agents & Robots
│   │   └── chapter-03/        # AI & Humanoid Robots
│   ├── src/
│   │   ├── components/        # React components (ChatBot, AuthModal)
│   │   ├── contexts/          # Auth context
│   │   ├── pages/             # Custom pages (onboarding, profile)
│   │   └── services/          # API clients
│   └── static/                # Static assets
│
├── 📁 specs/                  # Feature specifications
└── 📁 history/                # Development history
```

---

## ✨ Features

### 📖 Interactive Textbook
- **Chapter 1: The Rise of Physical AI** - Understanding the convergence of AI and physical systems
- **Chapter 2: Humans, Agents & Robots** - Exploring the future workforce dynamics
- **Chapter 3: AI & Humanoid Robots** - Deep dive into humanoid robotics technology

### 🤖 AI Assistant Chatbot
- **Context-Aware Responses** - Answers questions using textbook content
- **RAG Architecture** - Powered by OpenAI GPT-4o and Qdrant vector database
- **Streaming Responses** - Real-time SSE response generation
- **Text Selection Context** - Select text in the book and ask the AI about it

### 🔐 Authentication System (Better Auth)
- **Email/Password** - Register and login with email
- **Google OAuth** - Single sign-on with Google
- **JWT Tokens** - Secure token-based API authentication
- **User Profiles** - Track experience level and preferences

### 🎨 Modern UI/UX
- Dark theme optimized for reading
- Mobile-responsive design
- Smooth animations and transitions
- Accessible navigation

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20+
- **Python** 3.12+
- **uv** (Python package manager) - `pip install uv`

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ahmergit/hackathon-physical-ai-textbook.git
cd hackathon-physical-ai-textbook
```

### 2️⃣ Start Better Auth Service

```bash
cd backend/auth-ts
npm install
cp .env.example .env  # Configure environment variables
npm run dev
```

### 3️⃣ Start FastAPI Backend

```bash
cd backend
uv venv
uv pip install -r requirements.txt
cp .env.example .env  # Configure environment variables
uv run alembic upgrade head
uv run uvicorn src.main:app --reload --port 8000
```

### 4️⃣ Start Docusaurus Frontend

```bash
cd book-source
npm install
npm start
```

### 5️⃣ Access the Application

- **Frontend**: http://localhost:3000/physical-ai-humaniod-robotics/
- **Better Auth**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## ⚙️ Environment Variables

### Better Auth (`backend/auth-ts/.env`)

```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-secret
BETTER_AUTH_URL=http://localhost:3001
JWT_SECRET=shared-jwt-secret
TRUSTED_ORIGINS=http://localhost:3000
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### FastAPI Backend (`backend/.env`)

```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
SECRET_KEY=your-secret-key
JWT_SECRET=shared-jwt-secret  # Must match auth-ts
OPENAI_API_KEY=sk-your-openai-key
QDRANT_URL=https://your-qdrant-instance.cloud
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=physical-ai-textbook
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## 📡 API Endpoints

### Better Auth (Port 3001)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/sign-up/email` | Register with email |
| POST | `/api/auth/sign-in/email` | Login with email |
| GET | `/api/auth/sign-in/social?provider=google` | Google OAuth |
| GET | `/api/auth/session` | Get current session |
| POST | `/api/sync-user` | Sync user & get JWT |

### FastAPI Backend (Port 8000)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/stream` | Chat with AI (SSE) |
| GET | `/api/chat/health` | Health check |
| POST | `/api/users/sync` | Sync user from auth |
| GET | `/api/users/me` | Get current user |
| POST | `/api/profiles/onboarding` | Complete onboarding |
| GET | `/api/profiles/me` | Get profile |

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
uv run pytest
```

### Frontend Tests
```bash
cd book-source
npm test
```

### E2E Tests
```bash
cd book-source
npx playwright test
```

---

## 📖 Textbook Content

### Chapter 1: The Rise of Physical AI
1. Introduction to Physical AI
2. Key Components of Physical AI
3. Real-World Applications
4. Challenges & Limitations
5. The Future of Physical AI

### Chapter 2: Humans, Agents & Robots
1. The New Partnership Paradigm
2. Essential Human Capabilities
3. The Emergence of Hybrid Roles
4. Economic Transformations
5. Preparing for the Integrated Workforce

### Chapter 3: AI & Humanoid Robots
1. Why Humanoid Robots Matter Today & Tomorrow
2. Automation & Flexibility
3. Service & Care
4. Challenges & Ethics
5. Future Skills

---

## 🛠️ Tech Stack

### Frontend
- **Docusaurus 3.9** - Static site generator
- **React 18** - UI library
- **TypeScript** - Type safety
- **CSS Modules** - Styling

### Backend
- **FastAPI** - Python web framework
- **Better Auth** - TypeScript authentication
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation

### AI/ML
- **OpenAI GPT-4o** - Language model for chat
- **Qdrant Cloud** - Vector database for RAG
- **text-embedding-3-small** - Embeddings model

### Infrastructure
- **Neon PostgreSQL** - Cloud database
- **JWT** - Authentication tokens
- **SSE** - Real-time streaming

---

## 🚀 Deployment

### GitHub Pages (Frontend)
The frontend automatically deploys to GitHub Pages on push to `main`:
- URL: https://ahmergit.github.io/physical-ai-humaniod-robotics/

### Render (Backend)
Backend services can be deployed to Render using `render.yaml`.

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](book-source/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

Built with ❤️ for the Hackathon 2025

---

## 🙏 Acknowledgments

- [Docusaurus](https://docusaurus.io/) - Documentation framework
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [Better Auth](https://www.better-auth.com/) - Authentication library
- [OpenAI](https://openai.com/) - AI language models
- [Qdrant](https://qdrant.tech/) - Vector search engine
- [Neon](https://neon.tech/) - Serverless PostgreSQL

---

<p align="center">
  <b>Physical AI & Humanoid Robotics: From Fundamentals to Advanced Applications</b>
  <br>
  <sub>Bridging the gap between artificial intelligence and physical embodiment</sub>
</p>
