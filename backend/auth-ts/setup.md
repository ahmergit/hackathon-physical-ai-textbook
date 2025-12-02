# Auth Service Setup Instructions

## Step 1: Install Dependencies

```bash
cd backend/auth-ts
npm install
```

## Step 2: Configure Environment

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Edit `.env` with your values:
- `DATABASE_URL`: Your Neon PostgreSQL connection string (same as FastAPI)
- `JWT_SECRET`: Generate with `python -c "import secrets; print(secrets.token_urlsafe(48))"`
  - **CRITICAL**: This MUST match FastAPI's `JWT_SECRET` exactly!
- `GOOGLE_CLIENT_ID`: From Google Cloud Console
- `GOOGLE_CLIENT_SECRET`: From Google Cloud Console

## Step 3: Run Better Auth Database Migration

This creates the required tables (`user`, `session`, `account`, `verification`):

```bash
npx @better-auth/cli migrate
```

**Note**: This will prompt you for database connection. Use the same `DATABASE_URL` from your `.env` file.

## Step 4: Verify Tables Created

Connect to your database and verify these tables exist:
- `user`
- `session`
- `account`
- `verification`

## Step 5: Start Development Server

```bash
npm run dev
```

Server will start on http://localhost:3001

## Step 6: Test Health Endpoint

```bash
curl http://localhost:3001/health
```

Should return:
```json
{
  "status": "ok",
  "service": "auth-ts",
  "timestamp": "..."
}
```

## Next Steps

After auth-ts is running:
1. Run FastAPI backend (with JWT middleware)
2. Run frontend with updated auth components
3. Test authentication flows

## Troubleshooting

**"Cannot find module 'better-auth'"**
- Run `npm install` again

**"Connection refused" during migration**
- Check `DATABASE_URL` is correct
- Verify PostgreSQL is accessible
- Check firewall/network settings

**"JWT verification failed" from FastAPI**
- Verify `JWT_SECRET` matches exactly between auth-ts and FastAPI
- No extra whitespace or characters
