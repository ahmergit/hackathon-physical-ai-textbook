# Physical AI Auth Service (TypeScript)

Better Auth-based authentication service for the Physical AI Learning Platform.

## Features

- **Email/Password Authentication** (Primary method)
  - User signup with name, email, password
  - Secure password hashing with Better Auth
  - Login/logout functionality

- **Google OAuth** (Secondary method)
  - Single sign-on with Google accounts
  - Automatic user creation on first login

- **JWT Token Generation**
  - Access tokens (15-minute expiry)
  - Refresh tokens (7-day expiry)
  - Shared JWT secret with FastAPI backend

- **User Sync to PostgreSQL**
  - Syncs Better Auth users to legacy `users` table
  - Generates JWT tokens for FastAPI API access
  - Returns onboarding status

## Setup

### Prerequisites

- Node.js 18+
- PostgreSQL database (shared with FastAPI)
- Google OAuth credentials

### Installation

```bash
npm install
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
DATABASE_URL=postgresql://...
JWT_SECRET=<same-as-fastapi>
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

**CRITICAL**: `JWT_SECRET` MUST match FastAPI's `JWT_SECRET` exactly!

### Database Migration

Run Better Auth migration to create required tables:

```bash
npx @better-auth/cli migrate
```

This creates:
- `user` table (id, email, name, email_verified, created_at, updated_at)
- `session` table (session management)
- `account` table (OAuth provider accounts)
- `verification` table (email verification tokens)

### Development

```bash
npm run dev
```

Server runs on http://localhost:3001

### Production Build

```bash
npm run build
npm start
```

## API Endpoints

All Better Auth endpoints are available under `/api/auth/*`:

- `POST /api/auth/sign-up/email` - Email/password signup
- `POST /api/auth/sign-in/email` - Email/password login
- `GET /api/auth/google` - Google OAuth redirect
- `GET /api/auth/callback/google` - Google OAuth callback
- `POST /api/auth/sign-out` - Logout
- `GET /api/auth/session` - Get current session
- `POST /api/auth/refresh` - Refresh access token

### Custom Endpoints

- `POST /api/sync-user` - Sync Better Auth user to PostgreSQL, returns JWT tokens

## Architecture

```
Better Auth Session (HTTP-only cookie)
  ↓
/api/sync-user endpoint
  ↓
1. Verify session
2. Sync to legacy users table
3. Generate JWT tokens for FastAPI
4. Return accessToken + refreshToken
  ↓
Frontend stores tokens in localStorage
  ↓
API calls to FastAPI use Bearer tokens
```

## Integration with FastAPI

1. User authenticates via this service (email/password OR Google OAuth)
2. Frontend calls `/api/sync-user` to get JWT tokens
3. Tokens are sent to FastAPI with `Authorization: Bearer <accessToken>`
4. FastAPI verifies JWT using shared `JWT_SECRET`

## Security

- Passwords hashed with bcrypt (handled by Better Auth)
- JWT tokens signed with HS256 algorithm
- HTTP-only cookies for session management
- CORS configured for frontend and FastAPI origins
- Minimum password length: 8 characters

## Tech Stack

- **Better Auth**: Authentication framework
- **Express**: Web server
- **PostgreSQL**: Database (via pg driver)
- **TypeScript**: Type safety
- **JWT**: Token-based API authentication
