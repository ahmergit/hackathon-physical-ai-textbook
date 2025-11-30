---
id: 0001
title: Create Auth System Plan
stage: plan
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: auth-system
branch: 003-chapter2-workforce-physical-ai
user: developer
command: /sp.plan
labels: ["authentication", "planning", "better-auth-research", "fastapi-users", "database-schema", "api-contracts"]
links:
  spec: specs/auth-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/auth-system/plan.md
  - specs/auth-system/research.md
  - specs/auth-system/data-model.md
  - specs/auth-system/contracts/auth-api.yaml
  - specs/auth-system/contracts/profile-api.yaml
  - specs/auth-system/quickstart.md
tests:
  - No tests (planning phase)
---

## Prompt

Tech Stack: Python 3.13, FastAPI backend, Docusaurus frontend, Better Auth for email/password and Google SSO, Neon Serverless PostgreSQL, SQLAlchemy 2.0, Alembic, Tailwind CSS.

Backend Overview: FastAPI with layered architecture: routers, services, models, schemas, dependencies. Auth router handles signup, login, verification, sessions. Profile router manages user profiles. Services layer contains business logic and email integration via SendGrid.

Models & Schemas: User model stores name, email, hashed password, Better Auth ID, email_verified flag. Profile model stores programming/robotics experience, AI/ML experience, learning goals. EmailVerification model stores code, expiration, verified flag.

Session & Security: HTTP-only cookies for JWT access/refresh tokens. Passwords hashed with bcrypt. Access tokens 15 min, refresh 7 days. Rate limiting applied to signup/login/verify endpoints. CORS and security headers configured.

Email Verification: Generates unique code on signup, stores in email_verification table, sends email with verification link. Endpoint validates code, updates email_verified flag. Multiple unverified codes allowed per user; verified code activates account.

Frontend: Docusaurus React pages: Signup, Login, Email Verification, Onboarding. Signup supports email/password or Google SSO. Onboarding form captures robotics/programming background, AI/ML experience, learning goals. Hooks check session and protect routes.

User Flow: Signup → Onboarding → Email Verification → Login → Authenticated session. Verified users access protected resources with backend validation on each request.

Database: Three tables: users, profiles, email_verification. Normalized schema, foreign keys, cascade deletion, enum constraints, indexes for performance.

Authentication Flow: Backend validates signup/login requests, hashes passwords, creates profile, generates verification code, sends email. Login validates credentials, email verification, issues tokens.

Email Service: Templates rendered via Jinja2. SendGrid APIs used. Retry logic, HTML + plain text templates, expiration notice, security guidelines.

Testing: Pytest for unit/integration backend tests. React Testing Library and Playwright for frontend component and E2E testing. Coverage enforced, test automation on PRs.

Goal: Deliver a maintainable, secure, scalable, production-ready authentication and onboarding system with email verification, structured user profiles, and Google SSO support for Physical AI learning platform.

## Response snapshot

Created comprehensive implementation plan with Phase 0 (Research) and Phase 1 (Design & Contracts) completed.

**Phase 0: Research** (`research.md`, 50KB)

**Critical Finding**: Better Auth is TypeScript-only with NO official FastAPI integration. This fundamentally changed the architectural approach.

**Research Areas**:
1. Better Auth integration patterns → Concluded: Not viable for Python/FastAPI
2. FastAPI authentication approaches → Evaluated 4 options
3. Session management strategies → HTTP-only cookies with JWT
4. OAuth integration patterns → httpx-oauth for Google
5. CSRF protection mechanisms → SameSite=Lax + optional double-submit

**Final Recommendation**: **FastAPI-Users** (over Better Auth, custom JWT, Authlib-only, or DB sessions)

**Rationale**:
- ✅ Built-in email/password + OAuth (Google)
- ✅ Email verification with expiration
- ✅ HTTP-only cookies with security flags
- ✅ 15-minute JWT + 7-day session cookies
- ✅ Reduces dev time from 3-5 days to 1-2 days
- ✅ Production-tested, active maintenance (2025)

**Phase 1: Design** (`data-model.md`, `contracts/`, `quickstart.md`)

**Data Model**: 4 entities with relationships, constraints, indexes
1. **User** (FastAPI-Users base): id, email, hashed_password, is_verified, timestamps
2. **OAuthAccount**: Google OAuth credentials and tokens
3. **Profile**: robotics_experience, ai_ml_experience, learning_goals
4. **EmailVerification**: token (UUID), expires_at (24h), verification status

**API Contracts** (OpenAPI 3.1):
- `auth-api.yaml`: 8 endpoints (register, login, logout, verify, me, Google OAuth)
- `profile-api.yaml`: 2 endpoints (GET/POST profile with upsert logic)

**Quickstart Guide**: 8-section setup guide (45-minute estimated setup)
- Backend setup (FastAPI, dependencies, database, migrations)
- Frontend setup (Docusaurus, auth pages, hooks)
- Email service (SendGrid configuration, templates)
- Google OAuth (Cloud Console, credentials, consent screen)
- Testing procedures (unit, integration, E2E)
- Deployment checklists (Docker, static site, database)
- Troubleshooting (common issues with solutions)

**Project Structure Defined**:
- `backend/`: FastAPI layered architecture (routers, services, models, schemas, dependencies)
- `book-source/`: Docusaurus with custom auth pages, hooks, components
- Database migrations via Alembic
- Clear separation of concerns (auth logic, profile logic, email service)

## Outcome

- ✅ Impact: Complete implementation plan for authentication system with research-backed technology decisions, detailed data model, API contracts, and quickstart guide. Resolved Better Auth incompatibility early, pivoted to FastAPI-Users. All architecture decisions documented with rationale.
- 🧪 Tests: Planning phase - no tests. Testing strategy defined: pytest (backend unit/integration), Jest/React Testing Library (frontend components), Playwright (E2E).
- 📁 Files: Created 6 planning artifacts:
  - plan.md (implementation plan with constitution checks)
  - research.md (50KB: Better Auth evaluation, FastAPI-Users recommendation, security patterns)
  - data-model.md (database schema, migrations, query patterns)
  - contracts/auth-api.yaml (OpenAPI spec for 8 auth endpoints)
  - contracts/profile-api.yaml (OpenAPI spec for profile CRUD)
  - quickstart.md (45-minute setup guide with 8 sections)
- 🔁 Next prompts:
  1. Run `/sp.tasks` to generate implementation tasks from plan
  2. Run `/sp.adr` to document architectural decisions (FastAPI-Users choice, session strategy, database schema)
  3. Begin implementation: Install FastAPI-Users, create models, implement routers
  4. Frontend: Build signup/login/onboarding pages based on API contracts
- 🧠 Reflection: The Better Auth incompatibility discovery during research phase saved significant rework. FastAPI-Users provides exactly the required features (email/password + OAuth + email verification) with minimal custom code. Clear separation between planning artifacts (research, data model, contracts, quickstart) enables parallel implementation by multiple developers.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully. Better Auth incompatibility discovered early via research (not during implementation).
- Graders run and results (PASS/FAIL):
  - Constitution Check: PASS (all 10 principles satisfied)
  - Research Completeness: PASS (all NEEDS CLARIFICATION resolved)
  - Data Model Quality: PASS (normalized schema, proper indexes, constraints)
  - API Contract Clarity: PASS (OpenAPI 3.1 with examples, validation rules)
  - Quickstart Usability: PASS (step-by-step, estimated times, troubleshooting)
- Prompt variant (if applicable): Standard `/sp.plan` workflow with detailed tech stack input
- Next experiment (smallest change to try):
  1. Prototype FastAPI-Users integration in isolated environment before full implementation
  2. Test email verification flow end-to-end with SendGrid sandbox
  3. Validate Google OAuth callback handling with test Google account
