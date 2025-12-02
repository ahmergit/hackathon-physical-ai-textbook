# Physical AI Textbook - Backend

FastAPI backend service for the Physical AI Humanoid Robotics textbook platform, providing chatbot API, user management, and profile services.

## Architecture

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

- **Better Auth (auth-ts/)**: Handles authentication (email/password + Google OAuth)
- **FastAPI**: Chatbot API, user management, profiles
- **Neon PostgreSQL**: Cloud-hosted database with SSL

## Prerequisites

- Python 3.11+
- Node.js 20+ (for auth-ts)
- Neon PostgreSQL database

## Quick Start

### 1. Environment Setup

Create `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# JWT (must match auth-ts)
JWT_SECRET=your-jwt-secret

# OpenAI (for chatbot)
OPENAI_API_KEY=sk-...

# Optional
DEBUG=true
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
alembic upgrade head
```

### 4. Start Servers

```bash
# Terminal 1: Start Better Auth service
cd auth-ts
npm run dev

# Terminal 2: Start FastAPI backend
cd backend
uvicorn src.main:app --reload --port 8000
```

## API Endpoints

### Chatbot

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/chat/stream` | Stream chat response (SSE) | Required |
| GET | `/api/chat/health` | Health check | None |

**Chat Request:**
```json
{
  "message": "What is a humanoid robot?",
  "context": "Optional context from selected text"
}
```

### User Management

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/users/sync` | Sync user from auth | Required |
| GET | `/api/users/me` | Get current user | Required |

### Profiles

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/profiles/onboarding` | Complete onboarding | Required |
| GET | `/api/profiles/me` | Get current profile | Required |
| PUT | `/api/profiles/me` | Update profile | Required |

**Onboarding Request:**
```json
{
  "education_level": "college",
  "interests": ["robotics", "ai"],
  "onboarding_completed": true
}
```

## Project Structure

```
backend/
├── alembic/              # Database migrations
│   └── versions/
├── auth-ts/              # Better Auth service (TypeScript)
│   └── src/
├── src/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Configuration
│   ├── database.py       # Database connection
│   ├── middleware/
│   │   └── jwt_auth.py   # JWT token verification
│   ├── models/
│   │   ├── user.py       # User model
│   │   └── profile.py    # Profile model
│   ├── routers/
│   │   ├── chat.py       # Chat endpoints
│   │   ├── user.py       # User endpoints
│   │   └── profile.py    # Profile endpoints
│   └── services/
│       ├── user_manager.py
│       └── profile_service.py
└── tests/                # Test suite
```

## Authentication Flow

1. User authenticates via Better Auth (port 3001)
2. Better Auth issues JWT token stored in `better_auth.session_token` cookie
3. Frontend reads token and passes to FastAPI as `Authorization: Bearer <token>`
4. FastAPI validates JWT using shared `JWT_SECRET`
5. User data extracted from token for API requests

## Database Schema

### Tables (managed by Better Auth)
- `user` - Auth user accounts
- `session` - Active sessions
- `account` - OAuth accounts
- `verification` - Email verification tokens
- `jwks` - JSON Web Key Sets

### Tables (managed by Alembic)
- `users` - Application user data
- `profiles` - User profiles and preferences
- `alembic_version` - Migration tracking

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/unit/test_user_manager.py
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | Shared secret with auth-ts | Yes |
| `OPENAI_API_KEY` | OpenAI API key for chatbot | Yes |
| `DEBUG` | Enable debug mode | No |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) | No |

## Deployment

The backend is configured for Render deployment:

```yaml
# render.yaml
services:
  - type: web
    name: physical-ai-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

## Development Notes

- JWT tokens must be validated against the same secret used by auth-ts
- Database uses Neon PostgreSQL with SSL required
- Chat responses use Server-Sent Events (SSE) for streaming
- Profile education levels: `high_school`, `college`, `graduate`, `professional`
