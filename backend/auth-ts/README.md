# Better Auth Service

TypeScript authentication service using [Better Auth](https://www.better-auth.com/) for the Physical AI Textbook platform.

## Features

- 📧 Email/Password authentication
- 🔐 Google OAuth login
- 🔄 Session management
- 🎫 JWT token generation for FastAPI
- 👤 User sync to FastAPI backend

## Prerequisites

- Node.js 20+
- Neon PostgreSQL database
- Google OAuth credentials (optional)

## Quick Start

### 1. Install Dependencies

```bash
cd backend/auth-ts
npm install
```

### 2. Environment Setup

Create `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Auth
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:3001
TRUSTED_ORIGINS=http://localhost:3000

# JWT (must match FastAPI backend)
JWT_SECRET=your-jwt-secret

# Google OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 3. Run Development Server

```bash
npm run dev
```

Server runs on http://localhost:3001

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/sign-up/email` | Register with email/password |
| POST | `/api/auth/sign-in/email` | Login with email/password |
| GET | `/api/auth/sign-in/social?provider=google` | Start Google OAuth |
| GET | `/api/auth/callback/google` | Google OAuth callback |
| POST | `/api/auth/sign-out` | Sign out |
| GET | `/api/auth/session` | Get current session |

### User Sync

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/sync-user` | Generate JWT and sync user to FastAPI |

**Sync Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

## Project Structure

```
auth-ts/
├── src/
│   ├── index.ts          # Express server entry point
│   ├── auth.ts           # Better Auth configuration
│   └── routes/
│       └── sync-user.ts  # JWT generation & user sync
├── package.json
├── tsconfig.json
└── .env
```

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   Frontend      │────▶│  Better Auth    │────▶│    PostgreSQL    │
│   (React)       │     │   (Express)     │     │   (Neon Cloud)   │
└─────────────────┘     └────────┬────────┘     └──────────────────┘
                                 │
                                 │ JWT + User Data
                                 ▼
                        ┌─────────────────┐
                        │    FastAPI      │
                        │    Backend      │
                        └─────────────────┘
```

### Authentication Flow

1. **User authenticates** via Better Auth (email/password or Google)
2. **Session created** in PostgreSQL with session token
3. **Frontend calls** `/api/sync-user` to get JWT
4. **JWT generated** using shared `JWT_SECRET`
5. **User synced** to FastAPI backend
6. **Frontend stores** JWT for API requests

## Better Auth Configuration

Key settings in `src/auth.ts`:

```typescript
export const auth = betterAuth({
  database: new Pool({ connectionString: process.env.DATABASE_URL }),
  
  emailAndPassword: {
    enabled: true,
  },
  
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  
  trustedOrigins: [process.env.TRUSTED_ORIGINS || "http://localhost:3000"],
});
```

## Database Tables

Better Auth automatically manages these tables:

| Table | Description |
|-------|-------------|
| `user` | User accounts (id, email, name, etc.) |
| `session` | Active sessions with tokens |
| `account` | OAuth provider connections |
| `verification` | Email verification tokens |
| `jwks` | JSON Web Key Sets |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `BETTER_AUTH_SECRET` | Secret for session encryption | Yes |
| `BETTER_AUTH_URL` | Auth service URL | Yes |
| `JWT_SECRET` | Shared with FastAPI for token validation | Yes |
| `TRUSTED_ORIGINS` | Allowed CORS origins | Yes |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | No |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret | No |

## Development

```bash
# Run with hot reload
npm run dev

# Build for production
npm run build

# Run production build
npm start
```

## Integration with FastAPI

The auth service generates JWTs that FastAPI validates:

```python
# backend/src/middleware/jwt_auth.py
import jwt

def verify_token(token: str):
    payload = jwt.decode(
        token,
        os.getenv("JWT_SECRET"),
        algorithms=["HS256"]
    )
    return payload
```

**Important:** The `JWT_SECRET` must be identical in both services.
