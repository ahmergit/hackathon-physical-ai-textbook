# Physical AI Learning Platform - Auth Backend

FastAPI-based authentication, onboarding, and email verification system for the Physical AI Learning Platform.

## Features

- **Email/Password Authentication**: Secure user registration and login with FastAPI-Users
- **Email Verification**: SendGrid-powered verification emails with 24-hour expiration
- **Google OAuth 2.0**: Single sign-on with Google accounts
- **Session Management**: HTTP-only cookies with 15-minute JWT access tokens and 7-day refresh tokens
- **User Profiles**: Capture robotics/programming experience, AI/ML background, and learning goals
- **Async SQLAlchemy**: High-performance database operations with PostgreSQL

## Tech Stack

- **Python 3.13**: Latest Python with modern async/await patterns
- **FastAPI 0.104**: Modern web framework with automatic OpenAPI docs
- **FastAPI-Users 13.0**: Complete authentication solution with email + OAuth
- **SQLAlchemy 2.0**: Modern ORM with async support
- **Alembic**: Database migration management
- **Pydantic v2**: Data validation and settings management
- **SendGrid**: Transactional email service
- **PostgreSQL**: Production database (asyncpg driver)

## Quick Start

### 1. Prerequisites

- Python 3.13+
- PostgreSQL (or use Neon Serverless)
- SendGrid account (for email verification)
- Google Cloud Console project (for OAuth)

### 2. Installation

```bash
# Install dependencies with uv
uv add fastapi uvicorn[standard] fastapi-users[sqlalchemy,oauth] \
  httpx-oauth sqlalchemy alembic asyncpg sendgrid pydantic[email] \
  pydantic-settings python-jose[cryptography] passlib[bcrypt]

# Or with pip
pip install -r requirements.txt
```

### 3. Environment Setup

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and set your values:
# - DATABASE_URL: PostgreSQL connection string
# - SECRET_KEY: Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
# - SENDGRID_API_KEY: From SendGrid dashboard
# - GOOGLE_CLIENT_ID/SECRET: From Google Cloud Console
```

### 4. Database Setup

```bash
# Create database (if using local PostgreSQL)
createdb physicalai_dev

# Run migrations
alembic upgrade head
```

### 5. Run Development Server

```bash
# Using uvicorn directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or with environment variables
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/physicalai_dev \
SECRET_KEY=your-secret-key \
uvicorn src.main:app --reload
```

### 6. Verify Installation

Visit http://localhost:8000/docs to see the interactive API documentation.

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings and configuration
│   ├── database.py          # SQLAlchemy async engine
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic
│   ├── dependencies/        # FastAPI dependencies
│   └── utils/               # Utility functions
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   └── env.py               # Alembic config
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata & tools
└── .env.example            # Environment template
```

## API Endpoints

### Authentication
- `POST /auth/register` - Create new account with email/password
- `POST /auth/login` - Login with credentials
- `POST /auth/logout` - Logout and invalidate tokens
- `GET /auth/me` - Get current user info
- `POST /auth/verify` - Verify email with token
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token

### OAuth
- `GET /auth/google` - Initiate Google OAuth flow
- `GET /auth/google/callback` - Handle OAuth callback

### Profile
- `GET /profile` - Get user profile
- `POST /profile` - Create/update profile with onboarding data

### Health
- `GET /health` - Service health check
- `GET /` - API information

## Development

### Run Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/
```

### Code Formatting

```bash
black src/
```

### Linting

```bash
ruff check src/
```

### Create Migration

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Configuration

All configuration is managed through environment variables (see `.env.example`):

- **Database**: `DATABASE_URL`
- **Security**: `SECRET_KEY`, token expiration times
- **Email**: SendGrid API key and sender details
- **OAuth**: Google client credentials
- **CORS**: Frontend URL for cross-origin requests

## Security Features

- Passwords hashed with bcrypt
- HTTP-only cookies prevent XSS attacks
- JWT tokens with short expiration
- Email verification required before full access
- OAuth 2.0 state parameter prevents CSRF
- CORS configured for frontend origin only
- SQL injection protection via SQLAlchemy ORM

## Database Schema

### Users
- Core authentication data (email, hashed password)
- Email verification status and timestamps
- Active/inactive status

### OAuth Accounts
- Linked Google accounts
- OAuth provider details

### Profiles
- Robotics and programming experience levels
- AI/ML background
- Learning goals and preferences

### Email Verifications
- UUID tokens for email verification
- 24-hour expiration
- One-time use tokens

## License

MIT
