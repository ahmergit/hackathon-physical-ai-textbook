# Physical AI Authentication System - Quick Start Guide

## Prerequisites

- Python 3.13+
- Node.js 18+
- Neon PostgreSQL account (free tier: https://console.neon.tech)
- SendGrid account (free tier: https://signup.sendgrid.com)
- Google Cloud Console project (for OAuth)

## 5-Minute Setup

### Step 1: Clone and Navigate

```bash
cd C:\hackathon25\physical-ai-humaniod-robotics
```

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies with uv (recommended)
uv add fastapi uvicorn[standard] fastapi-users[sqlalchemy,oauth] httpx-oauth sqlalchemy alembic asyncpg sendgrid pydantic[email] pydantic-settings python-jose[cryptography] passlib[bcrypt] aiosqlite

# Create .env file
copy .env.example .env
```

**Edit `backend/.env`:**

```env
# 1. Get Neon PostgreSQL connection string from https://console.neon.tech
DATABASE_URL=postgresql+asyncpg://[user]:[password]@[endpoint]/neondb?sslmode=require

# 2. Generate secret key
SECRET_KEY=your-64-character-secret-key-change-this

# 3. Get SendGrid API key from https://app.sendgrid.com
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxx
FROM_EMAIL=noreply@yourdomain.com

# 4. Get Google OAuth credentials from https://console.cloud.google.com
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# 5. Frontend URL
FRONTEND_URL=http://localhost:3000
EMAIL_VERIFICATION_URL=http://localhost:3000/verify-email
```

**Run migrations:**

```bash
.venv/Scripts/alembic upgrade head
```

**Start backend server:**

```bash
uv run python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

### Step 3: Frontend Setup (Optional for API testing)

```bash
# In a new terminal
cd book-source

# Install dependencies
npm install axios react-hook-form zod @hookform/resolvers

# Configure environment
copy .env.example .env
```

**Edit `book-source/.env`:**

```env
API_BASE_URL=http://localhost:8000
```

**Start Docusaurus:**

```bash
npm run start
```

### Step 4: Verify Installation

**Test health endpoint:**

```bash
curl http://localhost:8000/health
```

**Expected response:**

```json
{
  "status": "healthy",
  "service": "physical-ai-auth",
  "version": "0.1.0",
  "environment": "development"
}
```

**Access API documentation:**

Open browser: http://localhost:8000/docs

---

## Quick Test Flow

### 1. Register a New User

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response:**

```json
{
  "id": "uuid",
  "email": "test@example.com",
  "is_active": true,
  "is_verified": false,
  "created_at": "2025-11-29T..."
}
```

**Check your email** for verification link (SendGrid will send it)

### 2. Verify Email (use token from email)

```bash
curl -X POST http://localhost:8000/auth/verify-email \
  -H "Content-Type: application/json" \
  -d '{
    "token": "uuid-token-from-email"
  }'
```

### 3. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=SecurePassword123!" \
  -c cookies.txt
```

**Response:**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### 4. Get Current User

```bash
curl http://localhost:8000/auth/me -b cookies.txt
```

### 5. Create Profile

```bash
curl -X POST http://localhost:8000/profile \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "robotics_experience": "beginner",
    "programming_experience": "intermediate",
    "ai_ml_experience": "none",
    "learning_goals": "I want to learn about humanoid robotics and build my first robot."
  }'
```

---

## Configuration Details

### Get Neon PostgreSQL Connection

1. Go to https://console.neon.tech
2. Create new project (free tier)
3. Copy connection string
4. Replace `DATABASE_URL` in `.env`

**Format:**
```
postgresql+asyncpg://[user]:[password]@[endpoint]/[database]?sslmode=require
```

### Get SendGrid API Key

1. Go to https://app.sendgrid.com
2. Settings → API Keys → Create API Key
3. Give it "Full Access" permission
4. Copy key and replace `SENDGRID_API_KEY` in `.env`

**Verify sender email:**
- Settings → Sender Authentication → Verify a Single Sender
- Use your email for `FROM_EMAIL`

### Get Google OAuth Credentials

1. Go to https://console.cloud.google.com
2. Create new project
3. Enable Google+ API
4. Credentials → Create Credentials → OAuth 2.0 Client ID
5. Application type: Web application
6. Authorized redirect URIs:
   - `http://localhost:3000/auth/google/callback`
   - `http://localhost:8000/auth/google/callback`
7. Copy Client ID and Client Secret

### Generate Secret Key

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy output and use for `SECRET_KEY` in `.env`

---

## Available Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with email/password
- `POST /auth/logout` - Logout current user
- `GET /auth/me` - Get current user

### Email Verification
- `POST /auth/verify-email` - Verify email with token
- `POST /auth/resend-verification` - Resend verification email

### Password Reset
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token

### Google OAuth
- `GET /auth/google/authorize` - Get authorization URL
- `GET /auth/google/callback` - OAuth callback

### Profile
- `GET /profile` - Get user profile
- `POST /profile` - Create profile (onboarding)
- `PUT /profile` - Update profile
- `DELETE /profile` - Delete profile

### Health
- `GET /health` - Health check
- `GET /` - API information

---

## Troubleshooting

### "Database connection failed"

**Solution:**
1. Verify Neon connection string is correct
2. Check your Neon project is not suspended (free tier)
3. Test connection: `psql "your-connection-string"`

### "Email not sending"

**Solution:**
1. Verify SendGrid API key is valid
2. Check sender email is verified in SendGrid
3. Review logs for errors: `tail -f backend/logs/app.log`

### "Invalid credentials" on login

**Solution:**
1. Ensure email is verified first
2. Check password meets requirements (min 3 chars)
3. Verify user exists: check `/auth/me` after registration

### "CORS error" from frontend

**Solution:**
1. Verify `CORS_ORIGINS` in `.env` includes frontend URL
2. Restart backend server after changing `.env`
3. Check browser console for specific CORS error

---

## Next Steps

1. ✅ Backend running on http://localhost:8000
2. ✅ API docs available at http://localhost:8000/docs
3. ✅ Database migrated and ready
4. 📝 Test all endpoints with Swagger UI
5. 🎨 Build frontend auth pages
6. 🚀 Deploy to production

---

## Production Deployment

### Update `.env` for production:

```env
# Use production database
DATABASE_URL=postgresql+asyncpg://prod-user:pass@prod-endpoint/prod-db?sslmode=require

# Use strong secret key
SECRET_KEY=generate-new-64-char-secret-for-production

# Production URLs
FRONTEND_URL=https://yourdomain.com
EMAIL_VERIFICATION_URL=https://yourdomain.com/verify-email

# Set environment
ENVIRONMENT=production

# Production CORS
CORS_ORIGINS=https://yourdomain.com
```

### Deploy backend:

```bash
# Install production dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start with production server (gunicorn)
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Deploy to cloud:

**Recommended platforms:**
- **Neon:** Database (already set up)
- **Render:** Backend API
- **Vercel:** Frontend (Docusaurus)
- **SendGrid:** Emails (already set up)

---

## Getting Help

- **API Documentation:** http://localhost:8000/docs
- **Implementation Guide:** [IMPLEMENTATION.md](IMPLEMENTATION.md)
- **Spec Documents:** `specs/auth-system/`
- **GitHub Issues:** Open an issue for bugs/questions

---

## Summary

✅ **Complete authentication system with:**
- Email/password registration
- Email verification (24-hour tokens)
- Google OAuth
- Profile management
- Password reset
- Session management
- HTTP-only cookies
- JWT authentication
- SendGrid email service
- Neon PostgreSQL database

🎉 **Ready to use!**

Start building your frontend auth pages or test the API with the Swagger UI at http://localhost:8000/docs
