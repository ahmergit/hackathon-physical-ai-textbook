# Quickstart Guide: Authentication System

**Feature**: Authentication, Onboarding, and Email Verification
**Date**: 2025-11-29
**Prerequisites**: Python 3.13, Node.js 18+, PostgreSQL access (Neon), SendGrid account, Google Cloud Console access

---

## Overview

This guide walks you through setting up the authentication system for local development, including:
- FastAPI backend with FastAPI-Users
- Neon Serverless PostgreSQL database
- Docusaurus frontend with custom auth pages
- SendGrid email service
- Google OAuth 2.0 integration

**Estimated Setup Time**: 30-45 minutes

---

## Prerequisites

### Required Software

- **Python 3.13+**: [Download](https://www.python.org/downloads/)
- **Node.js 18+ LTS**: [Download](https://nodejs.org/)
- **Git**: [Download](https://git-scm.com/)
- **PostgreSQL** (optional for local dev): [Download](https://www.postgresql.org/download/) or use SQLite

### Required Accounts

1. **Neon Serverless PostgreSQL**: [Sign up](https://neon.tech/)
2. **SendGrid**: [Sign up](https://sendgrid.com/) (free tier: 100 emails/day)
3. **Google Cloud Console**: [Sign up](https://console.cloud.google.com/)

---

## Part 1: Backend Setup (FastAPI)

### Step 1: Clone Repository and Navigate to Backend

```bash
git clone https://github.com/yourusername/physical-ai-humaniod-robotics.git
cd physical-ai-humaniod-robotics
mkdir backend
cd backend
```

### Step 2: Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt):
.\venv\Scripts\activate.bat

# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Create `requirements.txt`:
```txt
# Core Framework
fastapi==0.104.0
uvicorn[standard]==0.24.0

# Authentication
fastapi-users[sqlalchemy,oauth]==13.0.0
httpx-oauth==0.12.0

# Database
sqlalchemy==2.0.23
alembic==1.12.1
asyncpg==0.29.0  # PostgreSQL async driver
psycopg2-binary==2.9.9  # PostgreSQL sync driver (optional)

# Email
sendgrid==6.11.0
jinja2==3.1.2

# Validation & Security
pydantic[email]==2.5.0
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# CORS & Security Headers
python-dotenv==1.0.0

# Testing (optional)
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1

# Type Checking (optional)
mypy==1.7.1
```

Install:
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create `.env` file in `backend/` directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/physicalai_dev
# For Neon: postgresql+asyncpg://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Authentication
SECRET_KEY=your-super-secret-key-min-32-characters-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# SendGrid
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@physicalai.example.com
FROM_NAME=Physical AI Learning Platform

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Frontend URLs
FRONTEND_URL=http://localhost:3000
EMAIL_VERIFICATION_URL=http://localhost:3000/verify-email

# Environment
ENVIRONMENT=development
```

**Security Note**: NEVER commit `.env` to version control. Add to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

### Step 5: Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy output to `SECRET_KEY` in `.env`.

### Step 6: Set Up Database

#### Option A: Neon Serverless (Recommended for Production)

1. Go to [Neon Console](https://console.neon.tech/)
2. Create new project: "physical-ai-auth"
3. Copy connection string
4. Update `DATABASE_URL` in `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

#### Option B: Local PostgreSQL (Development)

```bash
# Create database
createdb physicalai_dev

# Update DATABASE_URL in .env
DATABASE_URL=postgresql+asyncpg://localhost:5432/physicalai_dev
```

#### Option C: SQLite (Quick Testing)

```env
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

### Step 7: Initialize Alembic (Database Migrations)

```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini to use .env DATABASE_URL
# (Set sqlalchemy.url to read from config)

# Edit alembic/env.py to import Base and models
```

Create first migration:
```bash
alembic revision --autogenerate -m "Initial schema: user, profile, email_verification"
```

Run migration:
```bash
alembic upgrade head
```

### Step 8: Create Backend Project Structure

```bash
mkdir -p src/{models,schemas,routers,services,dependencies,utils}
touch src/__init__.py
touch src/main.py src/config.py src/database.py
```

### Step 9: Run Backend Development Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify**: Navigate to http://localhost:8000/docs (FastAPI auto-generated Swagger docs)

---

## Part 2: Frontend Setup (Docusaurus)

### Step 1: Navigate to Frontend Directory

```bash
cd ../book-source
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Add Auth Dependencies

```bash
npm install axios react-hook-form zod @hookform/resolvers
```

### Step 4: Configure Environment Variables

Create `.env` file in `book-source/` directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

### Step 5: Create Auth Pages Structure

```bash
mkdir -p src/pages
mkdir -p src/components/auth
mkdir -p src/hooks
mkdir -p src/services
mkdir -p src/types
```

### Step 6: Run Frontend Development Server

```bash
npm start
```

**Verify**: Navigate to http://localhost:3000

---

## Part 3: Email Service Setup (SendGrid)

### Step 1: Create SendGrid Account

1. Sign up at [SendGrid](https://sendgrid.com/)
2. Verify your email address
3. Create API key:
   - Settings → API Keys → Create API Key
   - Name: "Physical AI Auth"
   - Permissions: "Full Access" or "Mail Send" only
   - Copy API key to `.env` as `SENDGRID_API_KEY`

### Step 2: Verify Sender Domain (Production)

1. Settings → Sender Authentication → Verify a Single Sender
2. Fill in sender details (name, email, address)
3. Verify email confirmation

**Development**: Use verified sender email as `FROM_EMAIL` in `.env`

### Step 3: Create Email Template (Optional)

SendGrid → Email API → Dynamic Templates → Create Template

Or use Jinja2 server-side templates (recommended for control).

### Step 4: Test Email Sending

```python
# backend/test_email.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def test_send_email():
    message = Mail(
        from_email=os.getenv('FROM_EMAIL'),
        to_emails='your-test-email@example.com',
        subject='Test Email from Physical AI',
        html_content='<strong>Email verification test successful!</strong>'
    )
    sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(f"Status Code: {response.status_code}")

if __name__ == "__main__":
    test_send_email()
```

Run:
```bash
python test_email.py
```

---

## Part 4: Google OAuth Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project: "Physical AI Auth"
3. Select project

### Step 2: Enable Google+ API

1. APIs & Services → Library
2. Search "Google+ API"
3. Click "Enable"

### Step 3: Configure OAuth Consent Screen

1. APIs & Services → OAuth consent screen
2. Select "External" user type
3. Fill in app information:
   - App name: "Physical AI Learning Platform"
   - User support email: your-email@example.com
   - Developer contact: your-email@example.com
4. Scopes: Add `email` and `profile`
5. Save and continue

### Step 4: Create OAuth 2.0 Credentials

1. APIs & Services → Credentials → Create Credentials → OAuth client ID
2. Application type: "Web application"
3. Name: "Physical AI Web Client"
4. Authorized redirect URIs:
   - **Development**: `http://localhost:8000/api/auth/google/callback`
   - **Production**: `https://api.physicalai.example.com/api/auth/google/callback`
5. Create
6. Copy Client ID and Client Secret to `.env`

### Step 5: Test OAuth Flow

1. Start backend: `uvicorn src.main:app --reload`
2. Navigate to: http://localhost:8000/api/auth/google/authorize
3. Authorize with Google account
4. Verify redirect to frontend with session cookie

---

## Part 5: Database Verification

### Step 1: Connect to Database

```bash
# For Neon:
psql "postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

# For local PostgreSQL:
psql physicalai_dev
```

### Step 2: Verify Tables Exist

```sql
\dt
```

Expected output:
```
           List of relations
 Schema |        Name        | Type  |  Owner
--------+--------------------+-------+---------
 public | user               | table | user
 public | oauth_account      | table | user
 public | profile            | table | user
 public | email_verification | table | user
 public | alembic_version    | table | user
```

### Step 3: Inspect Schema

```sql
\d user
\d profile
\d email_verification
```

Verify columns match data model (see `data-model.md`).

---

## Part 6: Testing the System

### End-to-End Test: Email/Password Registration

1. **Frontend**: Navigate to http://localhost:3000/signup
2. **Register**:
   - Email: test@example.com
   - Password: TestPass123!
3. **Verify**:
   - Check SendGrid Activity (SendGrid Dashboard → Activity)
   - Open verification email
   - Click verification link
4. **Login**: Navigate to http://localhost:3000/login
   - Email: test@example.com
   - Password: TestPass123!
5. **Onboarding**: Fill out profile form
6. **Access Protected Page**: Navigate to http://localhost:3000/profile

### End-to-End Test: Google OAuth

1. Navigate to http://localhost:3000/signup
2. Click "Sign in with Google"
3. Authorize with Google account
4. Complete onboarding form
5. Verify profile data saved

### Backend API Testing (Postman/cURL)

**Register User**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "api-test@example.com",
    "password": "SecurePass123!"
  }'
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "api-test@example.com",
    "password": "SecurePass123!"
  }' \
  --cookie-jar cookies.txt
```

**Get Current User** (protected endpoint):
```bash
curl -X GET http://localhost:8000/api/auth/me \
  --cookie cookies.txt
```

---

## Part 7: Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_auth_service.py

# Run integration tests
pytest tests/integration/
```

### Frontend Tests

```bash
cd book-source

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests (Playwright)
npx playwright test

# Run E2E tests in UI mode
npx playwright test --ui
```

---

## Part 8: Deployment

### Backend Deployment (Docker)

Create `Dockerfile`:
```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t physicalai-backend .
docker run -p 8000:8000 --env-file .env physicalai-backend
```

### Frontend Deployment

```bash
cd book-source

# Build static site
npm run build

# Deploy to Netlify, Vercel, or GitHub Pages
# Example (Netlify):
npm install -g netlify-cli
netlify deploy --prod --dir=build
```

### Database Migration (Production)

```bash
# Set production DATABASE_URL
export DATABASE_URL="postgresql+asyncpg://user:password@neon-host/neondb?sslmode=require"

# Run migrations
alembic upgrade head
```

---

## Troubleshooting

### Issue: Database Connection Error

**Symptom**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solutions**:
1. Verify DATABASE_URL format (async driver: `postgresql+asyncpg://`)
2. Check database is running: `psql -U user -d physicalai_dev`
3. For Neon, ensure `?sslmode=require` in connection string
4. Check firewall/network access

### Issue: Email Not Sending

**Symptom**: Verification email not received

**Solutions**:
1. Check SendGrid API key is correct
2. Verify sender email is authenticated (SendGrid dashboard)
3. Check spam folder
4. Review SendGrid Activity log for errors
5. Ensure `FROM_EMAIL` matches verified sender

### Issue: Google OAuth Redirect Error

**Symptom**: `redirect_uri_mismatch` error from Google

**Solutions**:
1. Verify redirect URI in Google Cloud Console matches exactly:
   - Development: `http://localhost:8000/api/auth/google/callback`
   - No trailing slash
   - Correct protocol (http vs https)
2. Check GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in `.env`
3. Ensure OAuth consent screen is configured

### Issue: CORS Errors in Frontend

**Symptom**: `Access to XMLHttpRequest... blocked by CORS policy`

**Solutions**:
1. Add frontend URL to backend CORS allowed origins:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:3000"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
2. Ensure `credentials: "include"` in frontend fetch requests

### Issue: Session Cookie Not Set

**Symptom**: User logged in but `/me` returns 401

**Solutions**:
1. Check cookie settings in backend (httponly=True, samesite="lax")
2. Verify frontend sends `credentials: "include"` in fetch
3. Ensure backend and frontend on same domain (or CORS configured)
4. Check browser console for cookie warnings

---

## Next Steps

After completing this quickstart:

1. **Implement User Flows**:
   - Build frontend signup/login pages (see `contracts/auth-api.yaml`)
   - Create onboarding form (see `contracts/profile-api.yaml`)
   - Add protected routes with `useAuth` hook

2. **Add Security Features**:
   - Implement rate limiting (slowapi or fastapi-limiter)
   - Add CSRF protection (fastapi-csrf-protect)
   - Set up security headers

3. **Monitoring & Logging**:
   - Configure structured logging (Python logging module)
   - Set up error tracking (Sentry)
   - Monitor database performance (Neon metrics)

4. **Testing**:
   - Write unit tests for all services (see `tests/unit/`)
   - Create integration tests for auth flows
   - Add E2E tests for user journeys (Playwright)

5. **Documentation**:
   - Update API docs (OpenAPI annotations)
   - Write user guide for signup/login
   - Document deployment process

---

## Helpful Resources

### Official Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI-Users Guide](https://fastapi-users.github.io/fastapi-users/)
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Docusaurus Docs](https://docusaurus.io/docs)
- [SendGrid API Documentation](https://docs.sendgrid.com/api-reference/mail-send/mail-send)
- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)

### Code Examples
- [FastAPI-Users Full Example](https://github.com/fastapi-users/fastapi-users/tree/master/examples)
- [FastAPI OAuth Example](https://github.com/tiangolo/fastapi/tree/master/docs_src/security)
- [Docusaurus Custom Pages](https://docusaurus.io/docs/creating-pages)

### Community Support
- [FastAPI Discord](https://discord.gg/fastapi)
- [FastAPI-Users Gitter](https://gitter.im/fastapi-users/community)
- [Docusaurus Discord](https://discord.gg/docusaurus)

---

## Support

For issues or questions:
1. Check [GitHub Issues](https://github.com/yourusername/physical-ai-humaniod-robotics/issues)
2. Review specification: `specs/auth-system/spec.md`
3. Consult data model: `specs/auth-system/data-model.md`
4. Review API contracts: `specs/auth-system/contracts/`

---

**Quickstart Complete!** You now have a fully functional authentication system with email verification, Google OAuth, and user profiles.
