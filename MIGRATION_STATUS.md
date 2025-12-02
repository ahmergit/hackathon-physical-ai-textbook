# Better Auth Migration Status

**Last Updated**: 2025-12-02
**Status**: Backend Complete ✅ | Frontend In Progress 🟡

---

## 🎯 Overview

Migrating from FastAPI-Users to Better Auth for the Physical AI Learning Platform:
- **Primary Auth**: Email/Password (name, email, password)
- **Secondary Auth**: Google OAuth
- **Architecture**: Separate TypeScript auth service + FastAPI API with JWT verification

---

## ✅ Completed (Backend)

### 1. TypeScript Auth Service (`backend/auth-ts/`)

**Created Files:**
- ✅ `package.json` - Dependencies and scripts
- ✅ `tsconfig.json` - TypeScript configuration
- ✅ `.env.example` - Environment template
- ✅ `.gitignore` - Git ignore patterns
- ✅ `README.md` - Setup documentation
- ✅ `setup.md` - Detailed setup instructions
- ✅ `src/index.ts` - Express server entry point
- ✅ `src/auth.ts` - Better Auth configuration (email/password + Google OAuth)
- ✅ `src/db.ts` - PostgreSQL connection pool
- ✅ `src/routes/sync-user.ts` - User sync & JWT generation endpoint
- ✅ `src/types/index.ts` - TypeScript interfaces

**Features:**
- Email/password authentication (PRIMARY)
- Google OAuth (SECONDARY)
- JWT plugin (15-min access, 7-day refresh)
- User sync to legacy `users` table
- `/api/sync-user` endpoint returns accessToken + refreshToken + needsOnboarding flag

**Next Steps for Auth Service:**
```bash
cd backend/auth-ts
npm install
npx @better-auth/cli migrate  # Create Better Auth tables
npm run dev  # Start on :3001
```

---

### 2. Database Migrations

**Alembic Migration:**
- ✅ `backend/alembic/versions/20251202_add_better_auth_profile_fields.py`

**Changes:**
- Created `skill_level` enum (beginner, intermediate, expert)
- Created `device_type` enum (cloud_laptop, rtx_gpu, physical_robot)
- Added 4 new profile columns:
  - `hardware_skill` (SkillLevel)
  - `programming_skill` (SkillLevel)
  - `ai_ml_skill` (SkillLevel)
  - `current_device` (DeviceType)
- Migrated existing data from old columns
- Dropped old columns (`ai_agents_experience`, `robotics_hardware_experience`)

**Run Migration:**
```bash
cd backend
alembic upgrade head
```

---

### 3. FastAPI Refactoring

**Modified Files:**
- ✅ `backend/src/config.py` - Added `jwt_secret` field
- ✅ `backend/src/models/profile.py` - Updated with SkillLevel, DeviceType enums and new fields
- ✅ `backend/src/schemas/profile.py` - Updated ProfileCreate/Update/Read with new fields
- ✅ `backend/src/routers/profile.py` - Uses `get_current_user` instead of `current_verified_user`
- ✅ `backend/src/routers/chat.py` - Added JWT authentication requirement
- ✅ `backend/src/main.py` - Removed auth/oauth routers

**New Files:**
- ✅ `backend/src/middleware/__init__.py` - Middleware package
- ✅ `backend/src/middleware/jwt_auth.py` - JWT verification middleware

**JWT Middleware Features:**
- `verify_jwt_token()` - Validates Better Auth JWT using shared JWT_SECRET
- `get_current_user()` - FastAPI dependency for protected routes
- `get_current_user_optional()` - Optional auth dependency

**Protected Routes Now:**
- `GET /api/profile` - Get user profile
- `POST /api/profile` - Create profile (onboarding)
- `PUT /api/profile` - Update profile
- `DELETE /api/profile` - Delete profile
- `POST /api/chat` - Chat with RAG bot (requires auth)

---

### 4. Files to Delete (Manual Review Recommended)

**⚠️ OLD FASTAPI-USERS CODE - DELETE THESE:**

```bash
# Routers
backend/src/routers/auth.py         # Old auth endpoints
backend/src/routers/oauth.py        # Old OAuth endpoints

# Dependencies
backend/src/dependencies/auth.py    # Old auth dependencies
backend/src/dependencies/user_db.py # Old user DB adapter

# Services
backend/src/services/user_manager.py       # Old user manager
backend/src/services/email_service.py      # Old email service (can keep if used elsewhere)

# Models
backend/src/models/email_verification.py   # Old email verification

# Schemas
backend/src/schemas/auth.py                # Old auth schemas (if exists)
backend/src/schemas/email_verification.py  # Old verification schemas (if exists)
```

**Dependencies to Remove from `requirements.txt`:**
```
fastapi-users[sqlalchemy]
httpx-oauth
```

**Install JWT Library:**
```bash
cd backend
pip install pyjwt
# Or with uv:
uv add pyjwt
```

---

## 🟡 In Progress (Frontend)

### Remaining Tasks:

1. **Install @better-auth/react**
   ```bash
   cd book-source
   npm install @better-auth/react
   ```

2. **Create Auth Client** (`book-source/src/lib/auth-client.ts`)

3. **Update AuthContext** (`book-source/src/contexts/AuthContext.tsx`)
   - Add `loginWithEmail()`, `signupWithEmail()`, `loginWithGoogle()`
   - Call `/api/sync-user` after Better Auth session established
   - Store accessToken/refreshToken in localStorage

4. **Update NavbarAuth** (`book-source/src/components/NavbarAuth/NavbarAuth.tsx`)
   - Add email/password signup/login form
   - Add Google OAuth button as secondary option

5. **Create OAuth Callback** (`book-source/src/pages/auth-callback.tsx`)
   - Handle Google OAuth redirect
   - Call `/api/sync-user`
   - Redirect to /onboarding or home

6. **Update Onboarding** (`book-source/src/pages/onboarding.tsx`)
   - Add 4 dropdown fields:
     - Hardware/Robotics Experience
     - Programming Experience
     - AI/ML Experience
     - Current Device/Setup
   - Submit to `/api/profile` with Bearer token

7. **Update API Client** (`book-source/src/services/api.ts`)
   - Add Bearer token to request headers
   - Handle 401 with token refresh logic

8. **Update render.yaml**
   - Add auth-ts service configuration
   - Update CORS settings

---

## 🔑 Critical Configuration

### Environment Variables (MUST Match!)

**Auth-TS (.env):**
```bash
DATABASE_URL=postgresql://...  # Same as FastAPI
JWT_SECRET=<64-char-secret>    # MUST MATCH FastAPI
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
AUTH_SERVICE_URL=http://localhost:3001
FRONTEND_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

**FastAPI (.env):**
```bash
DATABASE_URL=postgresql://...  # Same as Auth-TS
JWT_SECRET=<same-as-auth-ts>   # MUST MATCH Auth-TS
OPENAI_API_KEY=...
QDRANT_URL=...
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

**Generate JWT_SECRET:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

---

## 🚀 Testing Checklist

### Backend:
- [ ] Auth-TS service starts on :3001
- [ ] FastAPI starts on :8000
- [ ] `/api/profile` requires Bearer token
- [ ] `/api/chat` requires Bearer token
- [ ] Alembic migration runs successfully
- [ ] Better Auth tables exist in database

### Frontend:
- [ ] Email/password signup creates user
- [ ] Email/password login works
- [ ] Google OAuth redirects correctly
- [ ] Tokens stored in localStorage
- [ ] New users redirect to /onboarding
- [ ] Onboarding form has 4 fields
- [ ] Profile POST includes Bearer token
- [ ] Chat requires authentication

### End-to-End:
- [ ] Signup → Onboarding → Profile created
- [ ] Login → Chat works
- [ ] Token refresh on expiry
- [ ] Logout clears tokens

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│  Frontend (Docusaurus/React)                                    │
│  - Email/password forms                                         │
│  - Google OAuth button                                          │
│  - Stores accessToken/refreshToken in localStorage             │
└────────────┬────────────────────────────────────────────────────┘
             │
             ├──────────────────────────────────────┐
             │                                      │
             ▼                                      ▼
┌────────────────────────┐              ┌─────────────────────────┐
│ Auth-TS (Node/Express) │              │ FastAPI Backend         │
│ :3001                  │              │ :8000                   │
├────────────────────────┤              ├─────────────────────────┤
│ Better Auth            │              │ JWT Middleware          │
│ - Email/password       │              │ - Verifies JWT          │
│ - Google OAuth         │              │ - Extracts user_id      │
│ - JWT plugin           │              │                         │
│                        │              │ Protected Routes:       │
│ POST /api/sync-user    │──────────────│ - GET/POST /api/profile │
│ (returns JWT tokens)   │   Shared     │ - POST /api/chat        │
└──────────┬─────────────┘  JWT_SECRET  └───────────┬─────────────┘
           │                                        │
           └────────────┬───────────────────────────┘
                        │
                        ▼
              ┌──────────────────────┐
              │ Neon PostgreSQL      │
              ├──────────────────────┤
              │ Better Auth Tables:  │
              │ - user               │
              │ - session            │
              │ - account            │
              │ - verification       │
              │                      │
              │ Legacy Tables:       │
              │ - users (synced)     │
              │ - profiles (4 fields)│
              └──────────────────────┘
```

---

## 🎬 Next Steps

1. **Complete Frontend Implementation** (Est. 4-5 hours)
   - Install @better-auth/react
   - Create auth client and update AuthContext
   - Update UI components (NavbarAuth, onboarding)
   - Add OAuth callback handler
   - Update API client with Bearer tokens

2. **Deploy Auth-TS to Render** (Est. 1.5 hours)
   - Update render.yaml
   - Set environment variables
   - Run Better Auth migration on production DB

3. **Deploy Updated FastAPI** (Est. 1 hour)
   - Run Alembic migration
   - Update environment variables
   - Verify protected routes work

4. **Deploy Frontend** (Est. 30 min)
   - Update environment variables
   - Build and deploy to GitHub Pages

5. **End-to-End Testing** (Est. 2 hours)
   - Test all auth flows
   - Verify token refresh
   - Test onboarding
   - Test chat with authentication

**Total Remaining Time**: ~9 hours

---

## 📝 Notes

- Backend migration is **COMPLETE** ✅
- All FastAPI routes now use JWT Bearer tokens
- Profile model updated with 4 new enum fields
- Better Auth handles authentication, FastAPI handles RAG/chatbot
- Clean separation of concerns between services

**Ready to proceed with frontend implementation!** 🚀
