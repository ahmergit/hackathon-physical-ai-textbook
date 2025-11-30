# Physical AI Learning Platform - Authentication System Implementation

## Overview

Complete authentication, onboarding, and email verification system for the Physical AI Learning Platform, built with FastAPI, FastAPI-Users, and Neon Serverless PostgreSQL.

**Implementation Date:** November 29, 2025
**Status:** ✅ Complete and Tested
**Architecture:** FastAPI 0.104 + FastAPI-Users 13.0 + Neon PostgreSQL

---

## System Architecture

### Technology Stack

**Backend:**
- Python 3.13
- FastAPI 0.104 (async web framework)
- FastAPI-Users 13.0 (authentication framework)
- SQLAlchemy 2.0 (async ORM)
- Alembic (database migrations)
- Pydantic v2 (validation & settings)
- SendGrid (email service)
- httpx-oauth (Google OAuth)

**Database:**
- **Production:** Neon Serverless PostgreSQL
- **Development:** SQLite (optional fallback)
- Async driver: asyncpg

**Frontend:**
- Docusaurus 3.9.2
- React 18 + TypeScript
- Axios (API client)
- React Hook Form + Zod (form validation)

---

## Features Implemented

### ✅ User Authentication (US1 - Priority P1)
- Email/password registration
- Secure password hashing with bcrypt
- JWT-based authentication with HTTP-only cookies
- Login/logout endpoints
- Session management (15-minute access + 7-day refresh tokens)

### ✅ Email Verification (US1 - Priority P1)
- Automated verification emails via SendGrid
- UUID-based verification tokens
- 24-hour token expiration
- Resend verification endpoint
- Beautiful HTML email templates

### ✅ User Profile Management (US4 - Priority P3)
- Onboarding data collection
- Experience level tracking (robotics, programming, AI/ML)
- Learning goals and preferences
- Weekly time commitment
- CRUD operations for profiles

### ✅ Google OAuth Integration (US2 - Priority P2)
- Google Sign-In support
- OAuth callback handling
- Email-based account association
- Automatic verification for OAuth users

### ✅ Password Reset (US3 Extension)
- Forgot password flow
- Secure reset token generation
- Password reset emails

### ✅ Security Features
- HTTP-only cookies (XSS protection)
- CSRF protection (SameSite cookies)
- Bcrypt password hashing
- JWT token-based authentication
- Email verification requirement
- CORS configuration

---

## Database Schema

### Tables Created

**users**
- `id` (UUID, PK)
- `email` (String, unique, indexed)
- `hashed_password` (String)
- `is_active` (Boolean)
- `is_superuser` (Boolean)
- `is_verified` (Boolean)
- `created_at`, `updated_at` (DateTime)

**profiles**
- `id` (UUID, PK)
- `user_id` (UUID, FK → users.id, unique)
- `robotics_experience` (Enum: none/beginner/intermediate/advanced/expert)
- `programming_experience` (Enum)
- `ai_ml_experience` (Enum)
- `learning_goals` (Text)
- `preferred_learning_style` (String, optional)
- `weekly_time_commitment` (Integer, optional)
- `created_at`, `updated_at` (DateTime)

**email_verifications**
- `id` (UUID, PK)
- `user_id` (UUID, FK → users.id)
- `token` (String, unique, indexed)
- `email` (String)
- `expires_at` (DateTime)
- `is_used` (Boolean)
- `used_at` (DateTime, nullable)
- `created_at` (DateTime)

**oauth_accounts**
- `id` (UUID, PK)
- `user_id` (UUID, FK → users.id)
- `oauth_name` (String) - e.g., "google"
- `account_id` (String, indexed)
- `account_email` (String)
- `access_token` (String)
- `refresh_token` (String, nullable)
- `expires_at` (Integer, nullable)
- `created_at`, `updated_at` (DateTime)

---

## API Endpoints

### Authentication Endpoints

#### POST `/auth/register`
Register new user with email and password.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (201):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-11-29T..."
}
```

**Side Effect:** Sends verification email with 24-hour token.

---

#### POST `/auth/login`
Login with email and password.

**Request (form-urlencoded):**
```
username=user@example.com
password=SecurePassword123!
```

**Response (200):**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**Side Effect:** Sets HTTP-only cookie `physicalai_auth` for 7 days.

---

#### POST `/auth/logout`
Logout current user (clear cookies).

**Headers:**
```
Cookie: physicalai_auth=...
```

**Response (200):**
```json
{
  "detail": "Successfully logged out"
}
```

---

#### GET `/auth/me`
Get current authenticated user.

**Headers:**
```
Cookie: physicalai_auth=...
```

**Response (200):**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "is_active": true,
  "is_verified": true,
  "created_at": "2025-11-29T...",
  "updated_at": "2025-11-29T..."
}
```

---

### Email Verification Endpoints

#### POST `/auth/verify-email`
Verify email with token from email.

**Request:**
```json
{
  "token": "uuid-token-from-email"
}
```

**Response (200):**
```json
{
  "message": "Email verified successfully",
  "email": "user@example.com",
  "verified": true
}
```

**Side Effect:** Sends welcome email.

---

#### POST `/auth/resend-verification`
Resend verification email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "message": "Verification email sent successfully",
  "email": "user@example.com"
}
```

---

### Password Reset Endpoints

#### POST `/auth/forgot-password`
Request password reset email.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (202):**
```json
{
  "detail": "Password reset email sent"
}
```

---

#### POST `/auth/reset-password`
Reset password with token.

**Request:**
```json
{
  "token": "reset-token-from-email",
  "password": "NewSecurePassword456!"
}
```

**Response (200):**
```json
{
  "detail": "Password reset successfully"
}
```

---

### Google OAuth Endpoints

#### GET `/auth/google/authorize`
Get Google OAuth authorization URL.

**Response (200):**
```json
{
  "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?..."
}
```

---

#### GET `/auth/google/callback`
OAuth callback (handled by frontend redirect).

**Query Parameters:**
- `code`: Authorization code from Google
- `state`: CSRF protection token

**Response:** Redirects to frontend with auth cookie set.

---

### Profile Endpoints

#### GET `/profile`
Get current user's profile.

**Headers:**
```
Cookie: physicalai_auth=...
```

**Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "robotics_experience": "beginner",
  "programming_experience": "intermediate",
  "ai_ml_experience": "none",
  "learning_goals": "I want to build humanoid robots...",
  "preferred_learning_style": "hands-on",
  "weekly_time_commitment": 10,
  "created_at": "2025-11-29T...",
  "updated_at": "2025-11-29T..."
}
```

---

#### POST `/profile`
Create user profile (onboarding).

**Headers:**
```
Cookie: physicalai_auth=...
```

**Request:**
```json
{
  "robotics_experience": "beginner",
  "programming_experience": "intermediate",
  "ai_ml_experience": "none",
  "learning_goals": "I want to build humanoid robots and understand AI control systems.",
  "preferred_learning_style": "hands-on",
  "weekly_time_commitment": 10
}
```

**Response (201):** Same as GET response.

---

#### PUT `/profile`
Update user profile.

**Request (partial update allowed):**
```json
{
  "learning_goals": "Updated goals...",
  "weekly_time_commitment": 15
}
```

**Response (200):** Updated profile.

---

#### DELETE `/profile`
Delete user profile.

**Response (204):** No content.

---

## Email Templates

### Verification Email
**Subject:** Verify your email - Physical AI Learning Platform
**Template:** `backend/src/services/email_templates/verification.html`
**Features:**
- Professional gradient header
- Prominent CTA button
- Copy-paste URL fallback
- 24-hour expiration notice
- Responsive design

### Welcome Email
**Subject:** Welcome to Physical AI Learning Platform!
**Template:** `backend/src/services/email_templates/welcome.html`
**Features:**
- Celebration header
- Next steps checklist
- Resource links
- Getting started CTA

### Password Reset Email
**Subject:** Reset your password - Physical AI Learning Platform
**Template:** `backend/src/services/email_templates/password_reset.html`
**Features:**
- Security warning box
- 1-hour expiration notice
- Reset button
- Ignore instruction for non-requesters

---

## Configuration

### Environment Variables

Create `backend/.env` from `.env.example`:

```bash
# Neon PostgreSQL (Get from https://console.neon.tech)
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Generate secret key:
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=your-64-character-secret-key-here

# SendGrid (Get from https://app.sendgrid.com)
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@yourdomain.com

# Google OAuth (Get from https://console.cloud.google.com)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# Frontend
FRONTEND_URL=http://localhost:3000
EMAIL_VERIFICATION_URL=http://localhost:3000/verify-email

# Environment
ENVIRONMENT=development

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

---

## Setup Instructions

### 1. Backend Setup

```bash
cd backend

# Install dependencies with uv (recommended)
uv add fastapi uvicorn[standard] fastapi-users[sqlalchemy,oauth] \
  httpx-oauth sqlalchemy alembic asyncpg sendgrid pydantic[email] \
  pydantic-settings python-jose[cryptography] passlib[bcrypt]

# Or with pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection string and API keys

# Run database migrations
alembic upgrade head

# Start development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend Setup

```bash
cd book-source

# Install dependencies
npm install axios react-hook-form zod @hookform/resolvers

# Configure environment
cp .env.example .env
# Edit .env with API_BASE_URL=http://localhost:8000

# Start Docusaurus
npm run start
```

### 3. Access API

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Frontend:** http://localhost:3000

---

## Testing

### Manual Testing Flow

1. **Register User:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'
```

2. **Check Email** (SendGrid will send verification email)

3. **Verify Email:**
```bash
curl -X POST http://localhost:8000/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{"token":"token-from-email"}'
```

4. **Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=TestPass123!" \
  -c cookies.txt
```

5. **Get Current User:**
```bash
curl http://localhost:8000/auth/me -b cookies.txt
```

6. **Create Profile:**
```bash
curl -X POST http://localhost:8000/profile \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "robotics_experience":"beginner",
    "programming_experience":"intermediate",
    "ai_ml_experience":"none",
    "learning_goals":"Build humanoid robots"
  }'
```

---

## Security Best Practices

✅ **Implemented:**
- Passwords hashed with bcrypt (cost factor 12)
- HTTP-only cookies prevent XSS
- SameSite=Lax prevents CSRF
- Email verification required
- JWT tokens with short expiration (15 minutes)
- Refresh tokens for extended sessions (7 days)
- CORS restricted to frontend origin
- SQL injection protection via SQLAlchemy ORM
- Environment variables for secrets
- No secrets in version control

🔒 **For Production:**
- Set `ENVIRONMENT=production` to disable docs
- Use strong `SECRET_KEY` (64+ chars)
- Enable HTTPS (`cookie_secure=True` in production)
- Configure proper CORS origins
- Set up rate limiting
- Enable logging and monitoring
- Use managed database (Neon)
- Set up backup and recovery

---

## File Structure

```
backend/
├── src/
│   ├── main.py                 # FastAPI app with routers
│   ├── config.py               # Pydantic settings
│   ├── database.py             # SQLAlchemy async engine
│   ├── models/
│   │   ├── user.py            # User model (FastAPI-Users base)
│   │   ├── oauth.py           # OAuth account model
│   │   ├── profile.py         # User profile model
│   │   └── email_verification.py  # Email verification model
│   ├── schemas/
│   │   ├── user.py            # User Pydantic schemas
│   │   ├── profile.py         # Profile Pydantic schemas
│   │   └── email_verification.py  # Verification schemas
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── oauth.py           # Google OAuth endpoints
│   │   └── profile.py         # Profile CRUD endpoints
│   ├── services/
│   │   ├── email_service.py   # SendGrid email service
│   │   ├── user_manager.py    # FastAPI-Users manager
│   │   └── email_templates/   # Jinja2 HTML templates
│   │       ├── verification.html
│   │       ├── welcome.html
│   │       └── password_reset.html
│   └── dependencies/
│       ├── auth.py            # Auth backend & FastAPI-Users setup
│       └── user_db.py         # User database adapter
├── alembic/
│   ├── versions/              # Database migrations
│   └── env.py                 # Alembic config (async)
├── .env                       # Environment variables
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
└── pyproject.toml             # Project metadata

book-source/
├── src/
│   ├── types/
│   │   └── auth.ts            # TypeScript types for auth
│   └── services/
│       └── api.ts             # Axios API client
└── .env.example               # Frontend env template
```

---

## Next Steps

### Immediate (MVP Complete):
- ✅ User registration with email verification
- ✅ Login/logout with session management
- ✅ Profile creation and management
- ✅ Email service integration

### Phase 2 (Frontend):
- [ ] Create registration form component
- [ ] Create login form component
- [ ] Create email verification page
- [ ] Create profile onboarding form
- [ ] Integrate with Docusaurus auth context

### Phase 3 (Enhanced Features):
- [ ] Password strength indicator
- [ ] Email change flow
- [ ] Account deletion
- [ ] Admin dashboard
- [ ] User activity logging
- [ ] Rate limiting
- [ ] 2FA support

---

## Troubleshooting

### Database Connection Issues
```bash
# Test Neon connection
psql "postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Check Alembic migrations
cd backend && alembic current
```

### Email Not Sending
- Verify SendGrid API key is valid
- Check SendGrid sender authentication
- Review logs for email service errors
- Test with SendGrid API playground

### Authentication Errors
- Verify `SECRET_KEY` is set and consistent
- Check cookie settings match environment (HTTP vs HTTPS)
- Ensure CORS origins include frontend URL
- Verify token expiration times

---

## Performance Considerations

**Database:**
- Neon Serverless auto-scales
- Connection pooling configured
- Async operations throughout
- Indexes on email, tokens

**API:**
- Async/await for all I/O operations
- FastAPI automatic OpenAPI docs
- Pydantic validation caching
- HTTP-only cookies reduce network overhead

**Security:**
- Bcrypt hashing optimized for security/speed balance
- JWT tokens are stateless (no DB lookup)
- Email templates pre-compiled (Jinja2)

---

## License

MIT License - See LICENSE file for details.

---

## Support

**Documentation:** http://localhost:8000/docs
**Health Check:** http://localhost:8000/health
**Repository:** https://github.com/your-org/physical-ai-platform

For issues or questions, please open a GitHub issue.
