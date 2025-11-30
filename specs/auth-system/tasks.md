# Implementation Tasks: Authentication, Onboarding, and Email Verification System

**Feature**: Authentication System
**Branch**: `004-auth-onboarding-email-verification`
**Date**: 2025-11-29
**Total Tasks**: 72

---

## Summary

This task list implements the authentication system organized by user stories to enable independent development and testing. Each user story represents a complete, testable increment of functionality.

**User Story Priority Order**:
1. **US1** (P1): New User Registration with Email Verification — MVP core
2. **US3** (P1): Session Management and Protected Resources — Security critical
3. **US2** (P2): Google SSO Registration and Onboarding — UX enhancement
4. **US4** (P3): Profile Data Management — Personalization enabler
5. **US5** (P3): Email Verification Expiration and Resend — Recovery path

**MVP Scope**: User Story 1 (US1) + User Story 3 (US3) = Complete authentication with email verification and session management

**Recommended Approach**: Implement stories in order, testing each story independently before moving to the next.

---

## Phase 1: Project Setup & Infrastructure

**Goal**: Initialize project structure, configure dependencies, and set up development environment.

**Independent Test**: Project builds successfully, database connects, environment variables load correctly.

### Setup Tasks

- [x] T001 Create backend directory structure: `backend/src/{models,schemas,routers,services,dependencies,utils}`
- [x] T002 Create backend/requirements.txt with FastAPI 3.13, fastapi-users 13.0, SQLAlchemy 2.0, alembic, asyncpg, sendgrid, pydantic 2.x
- [x] T003 Create backend/pyproject.toml with project metadata and mypy strict configuration
- [x] T004 Create backend/.env.example with all required environment variables (DATABASE_URL, SECRET_KEY, SENDGRID_API_KEY, GOOGLE_CLIENT_ID, etc.)
- [x] T005 Create backend/src/config.py using pydantic-settings for environment variable management
- [x] T006 Create backend/src/database.py with async SQLAlchemy engine and session factory
- [x] T007 Initialize Alembic: `alembic init alembic` and configure alembic/env.py to use async engine
- [x] T008 Create backend/src/main.py with FastAPI app, CORS middleware, and health check endpoint
- [x] T009 [P] Create backend/.gitignore (exclude .env, __pycache__, venv/, *.pyc)
- [x] T010 [P] Create backend/README.md with setup instructions from quickstart.md
- [ ] T011 [P] Install frontend dependencies: `cd book-source && npm install axios react-hook-form zod @hookform/resolvers`
- [ ] T012 [P] Create book-source/.env.example with REACT_APP_API_URL and REACT_APP_GOOGLE_CLIENT_ID
- [x] T013 [P] Create book-source/src/types/auth.ts with TypeScript interfaces for User, Profile, Auth responses
- [x] T014 [P] Create book-source/src/services/api.ts with axios instance configured for credentials: "include"

**Acceptance**:
- ✅ Backend virtual environment created and dependencies installed
- ✅ Frontend dependencies installed
- ✅ `uvicorn src.main:app --reload` starts server on localhost:8000
- ✅ `npm start` starts frontend on localhost:3000
- ✅ GET /health returns 200 OK

---

## Phase 2: Foundational Components (Blocking Prerequisites)

**Goal**: Implement shared infrastructure required by all user stories: database models, authentication utilities, and email service.

**Independent Test**: Database migrations run successfully, email service sends test email, security utilities hash/verify passwords.

### Database Models & Migrations

- [x] T015 Create backend/src/models/user.py with FastAPI-Users SQLAlchemyBaseUserTableUUID (id, email, hashed_password, is_active, is_verified, timestamps)
- [x] T016 Create backend/src/models/profile.py with Profile model (user_id FK, robotics_programming_experience enum, ai_ml_experience enum, learning_goals text)
- [x] T017 Create backend/src/models/email_verification.py with EmailVerification model (user_id FK, token UUID, expires_at, created_at)
- [x] T018 Create backend/src/models/__init__.py importing all models for Alembic discovery
- [x] T019 Generate Alembic migration: `alembic revision --autogenerate -m "Initial schema: user, profile, email_verification"`
- [x] T020 Run migration: `alembic upgrade head` and verify tables exist in database

### Pydantic Schemas

- [x] T021 [P] Create backend/src/schemas/user.py with UserResponse, UserCreate schemas
- [x] T022 [P] Create backend/src/schemas/auth.py with RegisterRequest, LoginRequest, VerifyRequest schemas
- [x] T023 [P] Create backend/src/schemas/profile.py with ProfileRequest, ProfileResponse, ExperienceLevel enum

### Security & Email Utilities

- [x] T024 [P] Create backend/src/utils/security.py with password hashing functions (bcrypt via FastAPI-Users)
- [x] T025 [P] Create backend/src/utils/email_templates.py with Jinja2 template for verification email (HTML + plain text)
- [x] T026 Create backend/src/services/email_service.py with send_verification_email function using SendGrid API

**Acceptance**:
- ✅ Database tables created: user, oauth_account, profile, email_verification
- ✅ All schemas validate correctly with Pydantic
- ✅ Email service sends test verification email successfully
- ✅ Security utilities hash passwords and generate secure tokens

---

## Phase 3: User Story 1 (P1) - New User Registration with Email Verification

**Story Goal**: Enable users to create accounts with email/password, complete profile onboarding, verify email, and log in.

**Why First**: This is the MVP foundation. Without account creation and verification, no other features are accessible.

**Independent Test**:
1. Navigate to /signup
2. Fill email, password
3. Fill onboarding form (robotics experience, AI/ML experience, learning goals)
4. Submit registration
5. Check email inbox for verification link
6. Click verification link
7. Navigate to /login
8. Log in with credentials
9. Verify session cookie set and /me endpoint returns user data

**Acceptance Criteria**:
- ✅ User account created with is_verified=false
- ✅ Profile data stored in profiles table
- ✅ Verification email sent with 24-hour expiration token
- ✅ Clicking verification link sets is_verified=true
- ✅ Unverified users cannot log in
- ✅ Verified users receive session cookie on login

### Backend: User Registration & Email Verification

- [x] T027 [US1] Configure FastAPI-Users: Create backend/src/dependencies/auth.py with UserManager, get_user_manager, get_user_db
- [x] T028 [US1] Implement user registration endpoint in UserManager with email verification trigger
- [x] T029 [US1] Create backend/src/services/auth_service.py with create_verification_token function (UUID, 24-hour expiration)
- [x] T030 [US1] Integrate email_service.send_verification_email in registration flow
- [x] T031 [US1] Create backend/src/routers/auth.py with POST /auth/verify endpoint to validate verification token
- [x] T032 [US1] Implement verification logic: check token exists, not expired, set user.is_verified=true
- [x] T033 [US1] Create backend/src/routers/profile.py with POST /profile endpoint for onboarding data
- [x] T034 [US1] Implement backend/src/services/profile_service.py with create_or_update_profile upsert logic
- [x] T035 [US1] Add FastAPI-Users auth router to backend/src/main.py with /auth/register and /auth/login endpoints
- [x] T036 [US1] Configure CookieTransport in dependencies/auth.py with httponly=True, secure=True, samesite="lax", max_age=604800 (7 days)
- [x] T037 [US1] Modify UserManager.on_after_login to reject unverified users (check is_verified flag)

### Frontend: Signup, Onboarding, Verification Pages

- [x] T038 [P] [US1] Create book-source/src/pages/signup.tsx with email/password form using react-hook-form
- [x] T039 [P] [US1] Add form validation to signup.tsx: email format, password min 8 chars with uppercase/lowercase/number
- [x] T040 [P] [US1] Implement POST /auth/register API call in signup.tsx with error handling
- [x] T041 [P] [US1] Create book-source/src/pages/onboarding.tsx with profile form (robotics experience dropdown, AI/ML experience dropdown, learning goals textarea)
- [x] T042 [P] [US1] Implement POST /profile API call in onboarding.tsx after successful signup
- [x] T043 [P] [US1] Create book-source/src/pages/verify-email.tsx to handle verification callback with token query parameter
- [x] T044 [P] [US1] Implement GET /auth/verify API call in verify-email.tsx, display success/error message
- [x] T045 [P] [US1] Create book-source/src/pages/login.tsx with email/password form
- [x] T046 [P] [US1] Implement POST /auth/login API call in login.tsx with credentials: "include" for cookie storage
- [x] T047 [P] [US1] Add redirect logic to login.tsx: redirect to /profile or dashboard on successful login

### Testing (US1)

- [x] T048 [P] [US1] Write backend/tests/unit/test_auth_service.py with test_create_verification_token, test_token_expiration
- [x] T049 [P] [US1] Write backend/tests/integration/test_registration_flow.py: POST /register → verify email sent → POST /verify → user.is_verified=true
- [x] T050 [P] [US1] Write backend/tests/integration/test_login_unverified.py: unverified user login returns 403 with error message
- [x] T051 [P] [US1] Write book-source/tests/pages/signup.test.tsx testing form validation and API call
- [x] T052 [P] [US1] Write book-source/tests/e2e/registration-flow.spec.ts (Playwright): full signup → verify → login E2E test

**US1 Acceptance**:
- ✅ All 26 tasks completed
- ✅ Independent test passes end-to-end
- ✅ Tests cover happy path and error cases
- ✅ No blockers for US3

---

## Phase 4: User Story 3 (P1) - Session Management and Protected Resources

**Story Goal**: Authenticated users maintain sessions across page refreshes, can access protected endpoints, and log out to invalidate sessions.

**Why Second**: Essential security feature. Enables protecting content and maintaining user state.

**Independent Test**:
1. Log in (from US1)
2. Navigate to /profile (protected page)
3. Refresh browser → session persists
4. Make API call to GET /me → returns user data
5. Log out → session invalidated
6. Attempt to access /profile → redirected to /login

**Acceptance Criteria**:
- ✅ Session cookie persists across page refreshes
- ✅ Protected endpoints validate session and return user data
- ✅ Logout clears session cookie and invalidates server-side session
- ✅ Unauthenticated access to protected endpoints returns 401

### Backend: Session Management & Protected Endpoints

- [x] T053 [US3] Configure JWTStrategy in dependencies/auth.py with 15-minute access token lifetime
- [x] T054 [US3] Create get_current_user dependency in dependencies/auth.py using FastAPI-Users current_user pattern
- [x] T055 [US3] Add GET /auth/me endpoint to auth router with get_current_user dependency, returns UserResponse
- [x] T056 [US3] Add POST /auth/logout endpoint to auth router, clears session cookie (set Max-Age=0)
- [x] T057 [US3] Protect GET /profile and POST /profile endpoints with get_current_user dependency
- [x] T058 [US3] Add error handling in routers for 401 Unauthorized (invalid/missing session)

### Frontend: Auth State Management & Protected Routes

- [x] T059 [P] [US3] Create book-source/src/hooks/useAuth.ts hook with GET /auth/me call, returns {user, loading, isAuthenticated, logout}
- [x] T060 [P] [US3] Create book-source/src/components/AuthProvider.tsx context provider wrapping useAuth hook
- [x] T061 [P] [US3] Create book-source/src/components/ProtectedRoute.tsx component that redirects to /login if not authenticated
- [x] T062 [P] [US3] Wrap book-source/src/pages/profile.tsx with <ProtectedRoute> component
- [x] T063 [P] [US3] Add logout button to Docusaurus navbar (book-source/src/theme/Navbar/index.tsx or custom component)
- [x] T064 [P] [US3] Implement logout handler: call POST /auth/logout, clear local state, redirect to homepage
- [x] T065 [P] [US3] Display user email in navbar when authenticated (using AuthProvider context)

### Testing (US3)

- [x] T066 [P] [US3] Write backend/tests/integration/test_session_persistence.py: login → GET /me (valid) → logout → GET /me (401)
- [x] T067 [P] [US3] Write backend/tests/integration/test_protected_endpoints.py: access /profile without auth → 401
- [x] T068 [P] [US3] Write book-source/tests/hooks/useAuth.test.ts testing authentication state updates
- [x] T069 [P] [US3] Write book-source/tests/components/ProtectedRoute.test.tsx testing redirect logic
- [x] T070 [P] [US3] Write book-source/tests/e2e/session-management.spec.ts: login → refresh browser → still authenticated → logout → not authenticated

**US3 Acceptance**:
- ✅ All 18 tasks completed
- ✅ Independent test passes
- ✅ Sessions work reliably across page refreshes
- ✅ Protected content inaccessible to unauthenticated users

---

## Phase 5: User Story 2 (P2) - Google SSO Registration and Onboarding

**Story Goal**: Users can sign up and log in using their Google account, bypassing email verification (Google pre-verifies emails).

**Why Third**: UX enhancement that reduces friction but not critical for MVP. Email/password flow must work first.

**Independent Test**:
1. Navigate to /signup
2. Click "Sign in with Google" button
3. Complete OAuth flow on Google's consent screen
4. Redirected back to platform with account created (is_verified=true)
5. Fill onboarding form
6. Access platform successfully

**Acceptance Criteria**:
- ✅ Google OAuth button redirects to Google consent screen
- ✅ OAuth callback creates user account with is_verified=true
- ✅ New users directed to onboarding form
- ✅ Returning users skip onboarding and access platform

### Backend: Google OAuth Integration

- [x] T071 [P] [US2] Install httpx-oauth: add to requirements.txt
- [x] T072 [US2] Configure GoogleOAuth2 client in dependencies/auth.py with GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
- [x] T073 [US2] Add OAuth router to FastAPI-Users setup in main.py with /auth/google/authorize and /auth/google/callback
- [x] T074 [US2] Implement UserManager.on_after_register for OAuth users: set is_verified=true automatically
- [x] T075 [US2] Add OAuth account association logic: link OAuthAccount to User via user_id FK

### Frontend: Google SSO Button & Flow

- [x] T076 [P] [US2] Create book-source/src/components/GoogleSSOButton.tsx with redirect to /auth/google/authorize
- [x] T077 [P] [US2] Add <GoogleSSOButton /> to signup.tsx and login.tsx pages
- [x] T078 [P] [US2] Handle OAuth callback redirect in verify-email.tsx or create dedicated callback handler page
- [x] T079 [P] [US2] Redirect new OAuth users to /onboarding, returning users to /profile or dashboard

### Testing (US2)

- [x] T080 [P] [US2] Write backend/tests/integration/test_google_oauth.py: mock OAuth flow, verify user created with is_verified=true
- [x] T081 [P] [US2] Write book-source/tests/e2e/google-sso.spec.ts: E2E test with Google test account (requires Google OAuth test mode setup)

**US2 Acceptance**:
- ✅ All 11 tasks completed
- ✅ Independent test passes
- ✅ Google OAuth flow works end-to-end
- ✅ Both email/password and Google SSO coexist without conflicts

---

## Phase 6: User Story 4 (P3) - Profile Data Management

**Story Goal**: Authenticated users can view and update their learning profile (robotics experience, AI/ML experience, learning goals).

**Why Fourth**: Enables personalization features but not blocking. Can be implemented after core auth works.

**Independent Test**:
1. Log in (from US1 or US2)
2. Navigate to /profile
3. View current profile data
4. Update robotics experience from "beginner" to "intermediate"
5. Update learning goals text
6. Submit changes
7. Refresh page → verify updated data persists

**Acceptance Criteria**:
- ✅ GET /profile returns user's stored profile data
- ✅ POST /profile updates existing profile (upsert logic)
- ✅ Profile changes persist in database
- ✅ Frontend displays current data and allows editing

### Backend: Profile CRUD (Already partially implemented in US1)

- [x] T082 [US4] Add GET /profile endpoint to profile router with get_current_user dependency
- [x] T083 [US4] Implement profile_service.get_profile_by_user_id function
- [x] T084 [US4] Add validation in POST /profile to enforce ExperienceLevel enum values and learning_goals max length (2000 chars)

### Frontend: Profile Page

- [x] T085 [P] [US4] Update book-source/src/pages/profile.tsx with GET /profile call to load current data on mount
- [x] T086 [P] [US4] Add form fields to profile.tsx for editing robotics experience, AI/ML experience, learning goals
- [x] T087 [P] [US4] Implement save handler in profile.tsx: POST /profile with updated data
- [x] T088 [P] [US4] Display success message on successful save, error message on validation failure

### Testing (US4)

- [x] T089 [P] [US4] Write backend/tests/unit/test_profile_service.py: test_create_profile, test_update_profile, test_upsert_logic
- [x] T090 [P] [US4] Write backend/tests/integration/test_profile_api.py: GET /profile returns data, POST /profile updates record
- [x] T091 [P] [US4] Write book-source/tests/pages/profile.test.tsx: form loads data, submits updates correctly

**US4 Acceptance**:
- ✅ All 10 tasks completed
- ✅ Independent test passes
- ✅ Profile data editable and persists
- ✅ Validation prevents invalid enum values

---

## Phase 7: User Story 5 (P3) - Email Verification Expiration and Resend

**Story Goal**: Users can request a new verification email if the original expires (24 hours), ensuring a recovery path without blocking signup.

**Why Last**: Important for edge cases but not critical for happy path. Most users verify immediately.

**Independent Test**:
1. Create account (from US1)
2. Wait 25 hours (or manually set expires_at in past for testing)
3. Click expired verification link → receive error
4. Click "Resend Verification Email" button
5. Check inbox for new verification email
6. Click new verification link → account activated

**Acceptance Criteria**:
- ✅ Expired tokens return clear error message
- ✅ POST /auth/request-verify-token generates new token and invalidates old ones
- ✅ New verification email sent with fresh 24-hour expiration
- ✅ Rate limiting prevents abuse (max 3 requests per hour per email)

### Backend: Verification Expiration & Resend

- [x] T092 [US5] Add token expiration check in POST /auth/verify: if expires_at < now, return 400 with "VERIFY_USER_TOKEN_EXPIRED"
- [x] T093 [US5] Create POST /auth/request-verify-token endpoint in auth router
- [x] T094 [US5] Implement resend logic in auth_service: invalidate old tokens (mark as superseded or delete), generate new token, send email
- [x] T095 [US5] Add rate limiting to POST /auth/request-verify-token using slowapi or fastapi-limiter (3 requests per hour per email)

### Frontend: Resend Verification UI

- [x] T096 [P] [US5] Update verify-email.tsx to display "Resend Verification Email" button when token expired error occurs
- [x] T097 [P] [US5] Implement resend handler: POST /auth/request-verify-token with user's email
- [x] T098 [P] [US5] Display success message: "New verification email sent. Please check your inbox."
- [x] T099 [P] [US5] Add "Resend Verification" link to login.tsx for unverified users (show after login attempt with 403 error)

### Testing (US5)

- [x] T100 [P] [US5] Write backend/tests/integration/test_verification_expiration.py: verify with expired token returns error
- [x] T101 [P] [US5] Write backend/tests/integration/test_resend_verification.py: old token invalidated, new token works
- [x] T102 [P] [US5] Write backend/tests/unit/test_rate_limiting.py: verify rate limit blocks excessive resend requests

**US5 Acceptance**:
- ✅ All 11 tasks completed
- ✅ Independent test passes
- ✅ Users can recover from expired verification links
- ✅ Rate limiting prevents abuse

---

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Add production-ready features that span multiple user stories: error handling, logging, security headers, deployment configuration.

### Security & Production Readiness

- [x] T103 [P] Add CORS configuration to main.py with allowed origins from environment variable (FRONTEND_URL)
- [x] T104 [P] Add security headers middleware to main.py (HSTS, X-Content-Type-Options, X-Frame-Options)
- [x] T105 [P] Configure structured logging in main.py using Python logging module (JSON format for production)
- [x] T106 [P] Add global exception handler to main.py for unhandled errors (return 500 with generic message, log details)
- [x] T107 [P] Create backend/Dockerfile with multi-stage build (dependencies layer + app layer)
- [x] T108 [P] Create backend/.dockerignore (exclude venv/, .env, __pycache__, tests/)
- [x] T109 [P] Add docker-compose.yml for local development (backend + PostgreSQL)

### Frontend Polish

- [x] T110 [P] Add loading spinners to all async operations (signup, login, profile save)
- [x] T111 [P] Implement toast notifications for success/error messages across all pages
- [x] T112 [P] Add form field validation error display for all forms
- [x] T113 [P] Style auth pages with Tailwind CSS matching Docusaurus theme
- [x] T114 [P] Add favicon and meta tags to index.html for SEO

### Documentation & Deployment

- [x] T115 [P] Update backend/README.md with deployment instructions (Docker, environment variables, database migration)
- [x] T116 [P] Create .github/workflows/backend-ci.yml for automated testing and linting (pytest, mypy, pylint)
- [x] T117 [P] Create .github/workflows/frontend-ci.yml for automated testing and build (npm test, npm run build)
- [x] T118 [P] Document API endpoints in backend/README.md with example curl commands
- [x] T119 [P] Add OpenAPI tags and descriptions to all router endpoints for auto-generated docs

**Polish Acceptance**:
- ✅ All 17 tasks completed
- ✅ Application production-ready
- ✅ CI/CD pipeline runs tests automatically
- ✅ Documentation complete

---

## Task Summary

**Total Tasks**: 119
- **Setup & Infrastructure**: 14 tasks
- **Foundational**: 12 tasks
- **US1 (P1)**: 26 tasks
- **US3 (P1)**: 18 tasks
- **US2 (P2)**: 11 tasks
- **US4 (P3)**: 10 tasks
- **US5 (P3)**: 11 tasks
- **Polish**: 17 tasks

**Parallel Opportunities**: 58 tasks marked [P] can be executed in parallel within their phase

---

## Dependencies & Execution Order

### Story Dependencies (Must Complete In Order)

```
Phase 1 (Setup)
  ↓
Phase 2 (Foundational)
  ↓
Phase 3 (US1) ────┐
  ↓               │
Phase 4 (US3) ────┤ (All P1 stories must complete before P2/P3)
  ↓               │
Phase 5 (US2) ←───┘
  ↓
Phase 6 (US4)
  ↓
Phase 7 (US5)
  ↓
Phase 8 (Polish)
```

**Critical Path**: Setup → Foundational → US1 → US3 → Polish

**Parallel Branches**:
- After US3: US2, US4, US5 can be developed independently by different team members
- Within each phase: Tasks marked [P] can run in parallel

### Blocking Relationships

- **US1 blocks**: US3 (needs login), US2 (needs registration), US4 (needs profiles), US5 (needs verification)
- **US3 blocks**: All features requiring authentication
- **Foundational blocks**: All user stories (need database models, schemas, email service)

---

## Parallel Execution Examples

### Phase 3 (US1) Parallelization

**Team Member A** (Backend):
- T027-T037 (Auth service, routers, profile service)

**Team Member B** (Frontend):
- T038-T047 (Signup, onboarding, verification, login pages)

**Team Member C** (Testing):
- T048-T052 (Unit tests, integration tests, E2E tests)

All three can work simultaneously after T001-T026 complete.

### Phase 4 (US3) Parallelization

**Team Member A**: T053-T058 (Backend session management)
**Team Member B**: T059-T065 (Frontend auth state)
**Team Member C**: T066-T070 (Testing)

---

## Independent Test Criteria (Per User Story)

### US1: New User Registration with Email Verification
✅ Visitor creates account with email/password
✅ Profile data captured during onboarding
✅ Verification email received and link works
✅ Unverified users cannot log in
✅ Verified users log in and receive session cookie

### US3: Session Management and Protected Resources
✅ Logged-in users access /profile without re-authenticating
✅ Session persists across page refreshes
✅ GET /me returns user data with valid session
✅ Logout invalidates session
✅ Unauthenticated access to /profile redirects to /login

### US2: Google SSO Registration
✅ "Sign in with Google" redirects to OAuth consent
✅ OAuth callback creates account with is_verified=true
✅ New Google users complete onboarding
✅ Returning Google users skip onboarding

### US4: Profile Data Management
✅ GET /profile returns stored data
✅ User updates profile fields
✅ POST /profile persists changes
✅ Refresh page shows updated data

### US5: Email Verification Expiration
✅ Expired verification link returns error
✅ Resend verification generates new email
✅ New verification link activates account
✅ Rate limiting prevents spam

---

## MVP Recommendation

**Minimum Viable Product (MVP)**:
- Phase 1 (Setup): T001-T014
- Phase 2 (Foundational): T015-T026
- Phase 3 (US1): T027-T052
- Phase 4 (US3): T053-T070
- Subset of Phase 8: T103-T106 (security & error handling)

**Total MVP Tasks**: 70 tasks

**Estimated Timeline**:
- 1 developer: 2-3 weeks
- 2 developers (parallel): 1.5-2 weeks
- 3 developers (parallel): 1-1.5 weeks

**Post-MVP Enhancements** (in order):
1. Phase 5 (US2): Google SSO (+11 tasks, +2-3 days)
2. Phase 6 (US4): Profile management (+10 tasks, +2 days)
3. Phase 7 (US5): Verification expiration (+11 tasks, +2 days)
4. Phase 8 (remaining): Deployment, CI/CD (+11 tasks, +1-2 days)

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
✅ Task IDs sequential (T001-T119)
✅ [P] marker present for parallelizable tasks (58 tasks)
✅ [Story] labels present for user story phases (US1-US5)
✅ File paths specified in task descriptions
✅ Dependencies documented in execution order section
✅ Independent test criteria defined for each user story

---

**Tasks Generation Complete**: Ready for implementation in priority order (US1 → US3 → US2 → US4 → US5 → Polish)
