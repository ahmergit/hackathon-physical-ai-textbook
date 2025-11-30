# Implementation Plan: Authentication, Onboarding, and Email Verification System

**Branch**: `004-auth-onboarding-email-verification` | **Date**: 2025-11-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/auth-system/spec.md`

## Summary

Build a production-ready authentication and onboarding system for the Physical AI Learning Platform with:
- **Backend**: FastAPI 3.13 with Better Auth for email/password and Google SSO authentication
- **Frontend**: Docusaurus React custom pages for signup, login, onboarding, and profile management
- **Database**: Neon Serverless PostgreSQL with three tables (users, profiles, email_verification)
- **Security**: HTTP-only cookies for JWT tokens, bcrypt password hashing, email verification required
- **Session Management**: 15-minute access tokens, 7-day refresh tokens, secure cookie storage
- **Email Service**: SendGrid for verification emails with Jinja2 templates

## Technical Context

**Language/Version**: Python 3.13 (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI 3.13, Better Auth, SQLAlchemy 2.0, Alembic, Pydantic 2.x, SendGrid, React 18, Docusaurus 3.9.2, Tailwind CSS
**Storage**: Neon Serverless PostgreSQL (production), SQLite (development)
**Testing**: pytest + pytest-asyncio (backend), Jest + React Testing Library (frontend), Playwright (E2E)
**Target Platform**: Linux server (backend via Docker/serverless), Static CDN (frontend)
**Project Type**: Web application (backend + frontend separation)
**Performance Goals**:
- Login response: <500ms
- Signup with email send: <2s
- Email delivery: <30s
- Handle 100 concurrent users without degradation
**Constraints**:
- Email verification required for email/password accounts (security)
- Session tokens must be HTTP-only cookies (prevent XSS)
- Database queries <200ms p95
- Frontend auth state update <200ms
**Scale/Scope**:
- Expected initial scale: 1000 users
- 8 API endpoints, 5 frontend pages
- 3 database tables with indexes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Spec-Driven Development
- ✅ **PASS**: Detailed specification created at `specs/auth-system/spec.md` with 40 functional requirements
- ✅ **PASS**: All deliverables (backend endpoints, frontend pages, database schema) defined in spec

### Principle II: Single Source of Truth
- ✅ **PASS**: Spec defines all authentication behavior, API contracts, database schema
- ✅ **PASS**: Implementation will follow spec exactly; no manual deviations

### Principle III: Automation-First & Reproducible
- ✅ **PASS**: Database migrations via Alembic (scripted, version-controlled)
- ✅ **PASS**: Backend deployable via Docker/serverless config
- ✅ **PASS**: Frontend builds via `npm run build` (deterministic)
- ✅ **PASS**: Tests automated in CI/CD pipeline

### Principle IV: Code Quality & Type Safety
- ✅ **PASS**: Python strict type hints (mypy enforcement)
- ✅ **PASS**: TypeScript strict mode enabled
- ✅ **PASS**: Pydantic models for all request/response validation
- ✅ **PASS**: Layered architecture: routers → services → models

### Principle V: Testing & Validation
- ✅ **PASS**: Unit tests for auth logic, profile CRUD
- ✅ **PASS**: Integration tests for full signup→verify→login flow
- ✅ **PASS**: E2E tests for frontend user journeys
- ✅ **PASS**: Schema validation via Pydantic and SQLAlchemy

### Principle VI: Performance & UX Consistency
- ✅ **PASS**: Performance targets defined (<500ms login, <2s signup)
- ✅ **PASS**: Responsive design (mobile-first, Tailwind CSS)
- ✅ **PASS**: Consistent branding across Docusaurus site

### Principle VII: Content Accuracy & Integrity
- ✅ **PASS**: No placeholder content in production
- ✅ **PASS**: Email templates use real project branding
- ✅ **PASS**: Error messages clear and actionable

### Principle VIII: Separation of Concerns
- ✅ **PASS**: Layered backend architecture (routers, services, models, schemas)
- ✅ **PASS**: Frontend components modular (hooks, pages, utilities)
- ✅ **PASS**: Configuration separate from code (environment variables)

### Principle IX: Minimal & Sufficient Content
- ✅ **PASS**: Only essential auth features in MVP (signup, login, verify, profile)
- ✅ **PASS**: No over-engineering (no unnecessary abstractions)

### Principle X: Modularity & Maintainability
- ✅ **PASS**: Clear project structure (backend/, frontend/)
- ✅ **PASS**: Each module single responsibility (auth router, profile router)
- ✅ **PASS**: README documentation for setup and deployment

**GATE STATUS**: ✅ ALL CHECKS PASS — Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/auth-system/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan output)
├── research.md          # Phase 0 output (technology decisions, patterns)
├── data-model.md        # Phase 1 output (database schema, entities)
├── quickstart.md        # Phase 1 output (setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── auth-api.yaml    # OpenAPI spec for auth endpoints
│   └── profile-api.yaml # OpenAPI spec for profile endpoints
└── tasks.md             # Phase 2 output (/sp.tasks - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/                           # FastAPI backend
├── src/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app, CORS, middleware
│   ├── config.py                  # Environment variables, settings
│   ├── database.py                # SQLAlchemy engine, session
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py                # User model
│   │   ├── profile.py             # Profile model
│   │   └── email_verification.py  # EmailVerification model
│   ├── schemas/                   # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── auth.py                # SignupRequest, LoginRequest, etc.
│   │   ├── profile.py             # ProfileRequest, ProfileResponse
│   │   └── user.py                # UserResponse
│   ├── routers/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                # /auth/* endpoints
│   │   └── profile.py             # /profile endpoints
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Signup, login, verification logic
│   │   ├── email_service.py       # SendGrid integration
│   │   └── profile_service.py     # Profile CRUD
│   ├── dependencies/              # Dependency injection
│   │   ├── __init__.py
│   │   └── auth.py                # get_current_user, verify_token
│   └── utils/                     # Helpers
│       ├── __init__.py
│       ├── security.py            # Password hashing, token generation
│       └── email_templates.py     # Jinja2 template rendering
├── alembic/                       # Database migrations
│   ├── versions/
│   │   └── 001_initial_schema.py  # Users, profiles, email_verification
│   ├── env.py
│   └── alembic.ini
├── tests/
│   ├── unit/
│   │   ├── test_auth_service.py
│   │   ├── test_email_service.py
│   │   └── test_profile_service.py
│   ├── integration/
│   │   ├── test_auth_flow.py      # Signup→verify→login
│   │   └── test_profile_api.py
│   └── conftest.py                # Pytest fixtures
├── Dockerfile
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata, mypy config
└── README.md

book-source/                       # Docusaurus frontend (existing)
├── src/
│   ├── components/
│   │   ├── ProtectedRoute.tsx     # Auth guard component
│   │   ├── AuthProvider.tsx       # Auth context provider
│   │   └── GoogleSSOButton.tsx    # Google OAuth button
│   ├── hooks/
│   │   └── useAuth.ts             # Auth state management hook
│   ├── pages/
│   │   ├── signup.tsx             # Signup page (email + Google SSO)
│   │   ├── login.tsx              # Login page
│   │   ├── verify-email.tsx       # Email verification result
│   │   ├── onboarding.tsx         # User profile onboarding
│   │   └── profile.tsx            # View/edit profile
│   ├── services/
│   │   └── api.ts                 # API client (axios/fetch wrapper)
│   └── types/
│       └── auth.ts                # TypeScript types for auth
├── tests/
│   ├── components/
│   │   ├── ProtectedRoute.test.tsx
│   │   └── AuthProvider.test.tsx
│   ├── pages/
│   │   ├── signup.test.tsx
│   │   └── login.test.tsx
│   └── e2e/
│       ├── auth-flow.spec.ts      # Playwright E2E tests
│       └── profile.spec.ts
├── docusaurus.config.ts           # Add API_URL config
├── package.json                   # Add axios, react-hook-form
└── README.md

.github/
└── workflows/
    ├── backend-ci.yml             # Backend tests, linting, type checking
    └── frontend-ci.yml            # Frontend tests, build
```

**Structure Decision**: Web application with backend/frontend separation. Backend is standalone FastAPI app deployable independently. Frontend is part of existing Docusaurus site (`book-source/`) with custom React pages for auth flows. This aligns with project constitution (Docusaurus as primary frontend) and allows backend to be deployed separately (serverless, Docker, etc.).

## Complexity Tracking

> **No violations detected — all constitution checks pass.**

This section is intentionally left empty as there are no complexity violations to justify.

---

## Phase 0: Research & Technology Decisions

### Research Tasks

1. **Better Auth Integration Patterns**
   - Research: How to integrate Better Auth with FastAPI (official docs, examples)
   - Research: Better Auth session management with HTTP-only cookies
   - Research: Better Auth Google OAuth configuration
   - Decision needed: Use Better Auth's built-in session management vs. custom JWT implementation

2. **SendGrid Integration Best Practices**
   - Research: SendGrid Python SDK usage patterns
   - Research: Email template rendering (Jinja2 vs. SendGrid templates)
   - Research: Retry logic and error handling for email delivery
   - Decision needed: Template rendering approach (server-side Jinja2 vs. SendGrid dynamic templates)

3. **Neon PostgreSQL Connection Patterns**
   - Research: SQLAlchemy 2.0 async patterns with Neon Serverless
   - Research: Connection pooling configuration for serverless environments
   - Research: Migration strategies (Alembic best practices)
   - Decision needed: Async vs. sync SQLAlchemy (performance vs. complexity)

4. **Frontend Session Management**
   - Research: React hooks for auth state management (context vs. state library)
   - Research: HTTP-only cookie handling in frontend (automatic vs. manual)
   - Research: Protected route patterns in Docusaurus
   - Decision needed: Context API vs. Zustand/Redux for auth state

5. **Rate Limiting Implementation**
   - Research: FastAPI rate limiting libraries (slowapi, fastapi-limiter)
   - Research: Rate limiting strategies (IP-based, user-based, endpoint-based)
   - Decision needed: Rate limiting approach and thresholds

### Technology Decisions to Document

Each research task above will produce entries in `research.md` with format:
- **Decision**: [What was chosen]
- **Rationale**: [Why chosen, referencing requirements]
- **Alternatives Considered**: [Other options and why rejected]
- **Implementation Notes**: [Key patterns, gotchas, configuration]

---

## Phase 1: Design & Contracts

### 1. Data Model (`data-model.md`)

**Entities to Extract from Spec**:

1. **User Entity**
   - Fields: id (PK), email (unique), name, better_auth_id (FK), email_verified (boolean), created_at, updated_at
   - Relationships: One-to-One with Profile, One-to-Many with EmailVerification
   - Validation: Email format (Pydantic EmailStr), unique email constraint
   - Indexes: email, better_auth_id

2. **Profile Entity**
   - Fields: id (PK), user_id (FK, unique), robotics_programming_experience (enum), ai_ml_experience (enum), learning_goals (text), created_at, updated_at
   - Relationships: Belongs to User (one-to-one)
   - Validation: Experience enums ('none', 'beginner', 'intermediate', 'advanced', 'expert')
   - Indexes: user_id

3. **EmailVerification Entity**
   - Fields: id (PK), user_id (FK), code (unique), expires_at (timestamp), verified_at (nullable timestamp), created_at
   - Relationships: Belongs to User
   - Validation: Code uniqueness, expiration logic (24 hours)
   - Indexes: code, user_id, expires_at

**State Transitions**:
- User: `unverified` → `verified` (via email verification)
- EmailVerification: `pending` → `verified` (via verification endpoint)

### 2. API Contracts (`contracts/`)

**Endpoints from Functional Requirements**:

**Auth Router** (`/api/auth/`):
1. `POST /signup` — User registration (email/password)
2. `POST /login` — User login (email/password)
3. `POST /logout` — Session invalidation
4. `GET /verify-email` — Email verification (query param: code)
5. `POST /resend-verification` — Resend verification email
6. `GET /me` — Get current user info (protected)
7. `POST /google` — Google OAuth (Better Auth handles)

**Profile Router** (`/api/profile/`):
1. `GET /` — Get authenticated user's profile (protected)
2. `POST /` — Create/update profile (protected)

**OpenAPI Specification Files**:
- `contracts/auth-api.yaml` — All auth endpoints with request/response schemas
- `contracts/profile-api.yaml` — Profile endpoints with schemas

### 3. Quickstart Guide (`quickstart.md`)

**Sections**:
1. **Prerequisites**: Python 3.13, Node 18+, PostgreSQL (Neon account), SendGrid API key, Google OAuth credentials
2. **Backend Setup**:
   - Clone repo
   - Create virtual environment: `python -m venv venv`
   - Install dependencies: `pip install -r requirements.txt`
   - Configure `.env` (DATABASE_URL, SENDGRID_API_KEY, etc.)
   - Run migrations: `alembic upgrade head`
   - Start server: `uvicorn src.main:app --reload`
3. **Frontend Setup**:
   - Navigate to `book-source/`
   - Install dependencies: `npm install`
   - Configure `.env` (REACT_APP_API_URL)
   - Start dev server: `npm start`
4. **Testing**:
   - Backend tests: `pytest`
   - Frontend tests: `npm test`
   - E2E tests: `npx playwright test`
5. **Deployment**:
   - Backend: Docker build, deploy to serverless (AWS Lambda, Railway, etc.)
   - Frontend: `npm run build`, deploy to Netlify/Vercel/GitHub Pages
   - Database: Provision Neon instance, run migrations

---

## Phase 2: Task Breakdown

**NOT EXECUTED BY /sp.plan — This is handled by /sp.tasks command**

After completing Phase 0 (research.md) and Phase 1 (data-model.md, contracts/, quickstart.md), the `/sp.tasks` command will:
1. Read this plan.md, research.md, data-model.md, contracts/
2. Generate `tasks.md` with testable implementation tasks
3. Break down by priority (P1 MVP, P2 enhancements, P3 future)
4. Each task includes acceptance criteria, test cases, dependencies

---

## Architectural Decisions Requiring ADRs

After completing this plan, the following architectural decisions should be documented via `/sp.adr`:

1. **Better Auth vs. Custom JWT Implementation**
   - Decision context: Authentication layer choice
   - Scope: All auth endpoints, session management
   - Alternatives: Better Auth, custom JWT, Authlib, FastAPI-Users

2. **HTTP-Only Cookies vs. LocalStorage for Tokens**
   - Decision context: Session token storage
   - Scope: Security, XSS prevention
   - Alternatives: HTTP-only cookies (chosen), localStorage, sessionStorage

3. **Async vs. Sync SQLAlchemy**
   - Decision context: Database query patterns
   - Scope: Performance, code complexity
   - Alternatives: Async SQLAlchemy 2.0, sync SQLAlchemy

4. **Email Template Rendering Approach**
   - Decision context: Verification email generation
   - Scope: Email service integration
   - Alternatives: Server-side Jinja2 (chosen), SendGrid dynamic templates

5. **Frontend Auth State Management**
   - Decision context: Session state across React components
   - Scope: useAuth hook, AuthProvider
   - Alternatives: Context API (chosen), Zustand, Redux

**Suggestion**: After Phase 1 design completion, run:
```bash
/sp.adr "Better Auth Integration Strategy"
/sp.adr "Session Token Storage: HTTP-Only Cookies"
/sp.adr "Database Query Layer: Async SQLAlchemy 2.0"
```

---

## Risk Analysis & Mitigations

### Technical Risks

1. **Better Auth Learning Curve**
   - Impact: Delayed implementation, potential security issues
   - Likelihood: Medium
   - Mitigation: Phase 0 research includes Better Auth documentation review, example projects, test integration in isolated environment

2. **Neon Serverless Connection Pooling**
   - Impact: Database connection errors, performance degradation
   - Likelihood: Low (Neon handles pooling)
   - Mitigation: Test connection patterns in development, monitor connection metrics, implement retry logic

3. **Email Deliverability**
   - Impact: Users can't verify accounts
   - Likelihood: Medium (spam filters, configuration errors)
   - Mitigation: Use verified SendGrid domain, implement monitoring, provide resend verification option, test with multiple email providers

4. **Google OAuth Configuration**
   - Impact: SSO doesn't work
   - Likelihood: Medium (common misconfiguration)
   - Mitigation: Phase 0 research includes OAuth flow testing, verify redirect URIs in development, clear error messages for users

5. **Session Synchronization Across Tabs**
   - Impact: Logout in one tab doesn't affect other tabs
   - Likelihood: Low (acceptable for MVP)
   - Mitigation: Document behavior, consider BroadcastChannel API for future enhancement

### Security Risks

1. **Session Hijacking**
   - Impact: Unauthorized account access
   - Likelihood: Low (with HTTP-only cookies + HTTPS)
   - Mitigation: HTTP-only, Secure, SameSite cookies, HTTPS enforcement in production

2. **Password Brute Force**
   - Impact: Account compromise
   - Likelihood: Medium (without rate limiting)
   - Mitigation: Implement rate limiting (5 attempts per 15 minutes), account lockout after 10 failed attempts

3. **Email Verification Bypass**
   - Impact: Unverified accounts access system
   - Likelihood: Low (server-side validation)
   - Mitigation: Server-side email_verified check on every protected endpoint, never trust client claims

---

## Performance Optimization Plan

1. **Database Queries**
   - Index all foreign keys, email, better_auth_id
   - Use SELECT specific columns (not SELECT *)
   - Connection pooling via SQLAlchemy

2. **API Response Time**
   - Cache user profile data (Redis optional for future)
   - Async endpoints where beneficial (email sending)
   - Minimize database round-trips (join queries)

3. **Email Delivery**
   - Async email sending (don't block signup response)
   - Background task queue (Celery optional for future)
   - SendGrid batch API if sending multiple emails

4. **Frontend Bundle Size**
   - Code splitting for auth pages (lazy load)
   - Tree shaking for unused dependencies
   - Minimize Tailwind CSS (PurgeCSS in production)

---

## Testing Strategy

### Backend Testing

**Unit Tests** (pytest):
- Auth service: `test_create_user`, `test_verify_email`, `test_login_unverified_account`
- Email service: `test_send_verification_email`, `test_template_rendering`
- Profile service: `test_create_profile`, `test_update_profile`
- Security utils: `test_hash_password`, `test_verify_password`, `test_generate_token`

**Integration Tests** (pytest + test database):
- `test_signup_flow`: POST /signup → verify email sent → DB user created
- `test_verification_flow`: GET /verify-email → email_verified set to true
- `test_login_flow`: POST /login → session cookie set → GET /me returns user
- `test_protected_endpoint_without_auth`: 401 Unauthorized

**Coverage Target**: >80% for services, >90% for critical auth logic

### Frontend Testing

**Component Tests** (Jest + React Testing Library):
- `ProtectedRoute.test.tsx`: Redirects when not authenticated
- `useAuth.test.ts`: Updates state on login/logout
- `signup.test.tsx`: Form validation, API call on submit
- `login.test.tsx`: Error handling for invalid credentials

**E2E Tests** (Playwright):
- `auth-flow.spec.ts`: Full signup → verify → login → access protected page
- `google-sso.spec.ts`: Google OAuth flow (requires test Google account)
- `profile.spec.ts`: View and update profile

**Coverage Target**: >70% for components, 100% for critical user flows (E2E)

---

## Deployment Checklist

### Backend Deployment

- [ ] Environment variables configured (production DATABASE_URL, SENDGRID_API_KEY, etc.)
- [ ] Database migrations run: `alembic upgrade head`
- [ ] CORS configured for production frontend domain
- [ ] HTTPS enforced (Secure cookie flag)
- [ ] Rate limiting enabled
- [ ] Logging configured (structured logs, error tracking)
- [ ] Health check endpoint: `GET /health`
- [ ] Docker image built and pushed (if using containers)

### Frontend Deployment

- [ ] API_URL configured for production backend
- [ ] Docusaurus build succeeds: `npm run build`
- [ ] Static files deployed to CDN
- [ ] Google OAuth redirect URIs updated for production domain
- [ ] Environment variables set (REACT_APP_API_URL, GOOGLE_CLIENT_ID)

### Email & OAuth

- [ ] SendGrid domain verified
- [ ] Verification email template tested with multiple providers
- [ ] Google OAuth consent screen configured
- [ ] OAuth credentials created (client ID, secret)
- [ ] Redirect URIs added to Google Cloud Console

### Monitoring & Alerts

- [ ] Database connection monitoring
- [ ] API response time tracking
- [ ] Email delivery rate monitoring
- [ ] Error rate alerts (>1% failed requests)
- [ ] Session creation/validation metrics

---

## Next Steps

1. **Phase 0 Execution** (Research):
   - Execute research tasks above
   - Document decisions in `research.md`
   - Resolve all NEEDS CLARIFICATION items

2. **Phase 1 Execution** (Design):
   - Generate `data-model.md` from entities above
   - Create OpenAPI specs in `contracts/`
   - Write `quickstart.md` with setup instructions
   - Update agent context: `.specify/scripts/bash/update-agent-context.sh claude`

3. **Re-check Constitution** (Post-Design):
   - Verify all gates still pass
   - Document any necessary complexity exceptions

4. **ADR Creation** (Recommended):
   - Run `/sp.adr "Better Auth Integration Strategy"`
   - Run `/sp.adr "Session Token Storage Strategy"`
   - Run `/sp.adr "Database Layer Architecture"`

5. **Task Breakdown** (/sp.tasks):
   - After Phase 0 and Phase 1 complete
   - Run `/sp.tasks` to generate implementation tasks

---

**PLAN STATUS**: ✅ Ready for Phase 0 Research

**Branch**: `004-auth-onboarding-email-verification` (to be created)
**Next Command**: Execute Phase 0 research tasks below
