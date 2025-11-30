---
id: 001
title: Create Authentication System Specification
stage: spec
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: auth-system
branch: 003-chapter2-workforce-physical-ai
user: developer
command: /sp.specify
labels: ["authentication", "onboarding", "email-verification", "better-auth", "fastapi", "docusaurus"]
links:
  spec: specs/auth-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/auth-system/spec.md
tests:
  - No tests (specification phase)
---

## Prompt

Physical AI Learning Platform — Authentication, Onboarding, and Email Verification System

[PURPOSE]
This specification defines a full-stack authentication and onboarding system for the Physical AI learning platform. The system ensures secure user registration and login, supports both email/password and Google SSO authentication, and implements email verification to confirm account validity. Additionally, it captures structured user profile information—including robotics/programming background, AI/ML experience, and learning goals—during signup to enable personalized learning experiences. The system is designed to be robust, maintainable, and fully integrated with the Docusaurus frontend.

[WHAT TO BUILD]

Backend: A FastAPI 3.13 server implementing Better Auth as the authentication layer. It must handle signup, login, session issuance, session validation, email verification, and user profile management. The backend will maintain clear separation between authentication data and user profile data stored in Neon Serverless PostgreSQL. Sessions will use secure HTTP-only cookies for token storage. A dedicated email_verification table must store codes with expiration timestamps, and a verification endpoint will validate the code to activate accounts. Routes include /signup, /login, /verify-email, /me, and /profile. All endpoints must be typed with Pydantic models and enforce access control via dependency injection.

Frontend: Docusaurus-based custom React pages for Signup, Login, Email Verification, and Onboarding forms. Signup supports email/password and Google SSO. After signup, the onboarding form collects the three structured fields (robotics/programming experience, AI/ML experience, learning goals). The frontend must submit these inputs to the backend API, trigger email verification, and handle session management via secure cookies. Hooks must check session validity, protect authenticated pages, and allow for content personalization based on stored user profile data.

Email Verification Flow: On account creation, generate a unique verification code, store it in the email_verification table with expiration, and send an email containing a clickable verification link. The verification endpoint confirms the code, sets the email_verified flag, and activates the account. Only verified users may log in.

Database: Neon Serverless PostgreSQL with three main tables:

users — stores name, email, Better Auth ID, email verification flag, and session reference.

profiles — stores robotics/programming experience, AI/ML experience, and learning goals.

email_verification — stores verification code, associated user ID, and expiration timestamp.

User Flow: Users visit the Signup page, create an account with email/password or Google SSO, fill out the onboarding form, and receive a verification email. Upon clicking the link, the backend validates the code and activates the account. Verified users can log in, initiating a secure session via cookies. All authenticated requests to protected resources are validated server-side.

[DELIVERABLES]

FastAPI backend with Better Auth integration, email verification workflow, and typed endpoints.

Docusaurus frontend pages with Signup, Login, Email Verification, and Onboarding forms.

Session management with secure cookies and dependency-injected protected endpoints.

Structured storage of user profile data linked to verified accounts.

Complete, maintainable, secure, and production-ready system ready for future personalization features.

[GOAL]
Deliver a stable, secure, and reproducible authentication and onboarding system that fully integrates with the Physical AI learning platform, captures structured user data, enforces email verification, and supports both traditional and Google-based authentication methods, ensuring a seamless and secure user experience.

## Response snapshot

Created comprehensive feature specification for the Physical AI Learning Platform authentication system at specs/auth-system/spec.md

**Key Components Specified:**

1. **Prioritized User Stories (5 stories)**:
   - P1: New User Registration with Email Verification (MVP critical path)
   - P2: Google SSO Registration and Onboarding (UX improvement)
   - P1: Session Management and Protected Resources (security critical)
   - P3: Profile Data Management (enabler for future features)
   - P3: Email Verification Expiration and Resend (recovery path)

2. **Functional Requirements (40 FRs)** covering:
   - Authentication & Account Management (FR-001 to FR-010)
   - Email Verification (FR-011 to FR-019)
   - Onboarding & Profile Management (FR-020 to FR-025)
   - Session Management (FR-026 to FR-031)
   - Frontend Integration (FR-032 to FR-040)

3. **Database Schema**:
   - `users` table: id, email, name, better_auth_id, email_verified, timestamps
   - `profiles` table: id, user_id, robotics_programming_experience, ai_ml_experience, learning_goals, timestamps
   - `email_verification` table: id, user_id, code, expires_at, verified_at, created_at
   - Indexes on all foreign keys and lookup columns

4. **API Endpoints** (7 endpoints):
   - POST /api/auth/signup (email/password registration)
   - POST /api/auth/google (Google SSO)
   - POST /api/auth/login (email/password login)
   - POST /api/auth/logout (session invalidation)
   - GET /api/auth/verify-email (email verification)
   - GET /api/auth/me (current user data)
   - GET/POST /api/profile (profile CRUD)
   - POST /api/auth/resend-verification (resend email)

5. **Frontend Pages** (7 pages/components):
   - /signup page with email/password and Google SSO
   - /login page with both auth methods
   - /verify-email result page
   - /onboarding form page
   - /profile page for viewing/editing
   - useAuth hook for session management
   - ProtectedRoute component for access control

6. **Security Measures**:
   - HTTP-only, Secure, SameSite cookies for session tokens
   - Better Auth for password hashing (bcrypt/argon2)
   - Pydantic validation for all inputs
   - Parameterized SQL queries (SQLAlchemy ORM)
   - XSS prevention via React defaults
   - CSRF protection via SameSite cookies
   - 24-hour verification code expiration
   - Rate limiting recommendations

7. **Success Criteria (10 metrics)**:
   - Account creation in <3 minutes
   - Email verification success rate >99%
   - Login response time <500ms
   - 100 concurrent users without degradation
   - 95% email verification within 24 hours
   - Zero unhandled auth errors in production

8. **Open Questions for Clarification**:
   - Email service selection (SendGrid, AWS SES, SMTP?)
   - Rate limiting implementation (yes/no, thresholds?)
   - Session duration preferences (7 days default?)
   - Onboarding mandatory vs skippable?
   - Password reset flow inclusion?
   - Learning goals format (free text, checkboxes, both?)
   - Account linking behavior for duplicate emails?

9. **Risk Analysis**:
   - Email deliverability issues → Use reputable service, monitoring
   - Better Auth integration complexity → Follow documentation, test thoroughly
   - Google OAuth misconfiguration → Test in dev first, verify URIs
   - Session hijacking/XSS → HTTP-only cookies, input sanitization
   - Database connection issues → Retry logic, monitoring, pooling

10. **Edge Cases Addressed**:
    - Duplicate email registration
    - Expired verification links
    - Google SSO with existing email/password account
    - Email service failures
    - Session expiration during use
    - SQL injection/XSS attempts
    - Lost verification emails
    - Multiple simultaneous sessions

## Outcome

- ✅ Impact: Comprehensive, production-ready specification for full authentication system covering backend (FastAPI + Better Auth), frontend (Docusaurus React pages), database (Neon PostgreSQL), email verification, session management, and user profiling. Spec provides clear contracts for all 40 functional requirements with acceptance criteria.
- 🧪 Tests: Specification phase - no tests yet. Testing strategy documented with 4 categories (unit, integration, frontend, E2E) covering 20+ test scenarios.
- 📁 Files: Created specs/auth-system/spec.md (15,000+ words, fully detailed specification)
- 🔁 Next prompts:
  1. User reviews spec and answers open questions (email service, rate limiting, session duration, etc.)
  2. Run `/sp.plan` to create architectural plan with detailed design decisions
  3. Run `/sp.tasks` to break down into testable implementation tasks
  4. Consider `/sp.adr` for architectural decisions (Better Auth choice, session strategy, database schema)
- 🧠 Reflection: Specification follows Spec-Driven Development principles with clear separation between business requirements (user stories), technical requirements (FRs), and implementation details (API contracts, database schema). Prioritized user stories enable incremental delivery (P1 stories = MVP). Open questions identified proactively to avoid implementation blockers.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification created successfully
- Graders run and results (PASS/FAIL):
  - Spec Template Compliance: PASS (all mandatory sections filled)
  - User Story Quality: PASS (prioritized, testable, independent)
  - Requirement Clarity: PASS (40 FRs with clear acceptance criteria)
  - Technical Feasibility: PASS (uses proven tech stack - FastAPI, Better Auth, Docusaurus, Neon)
  - Security Considerations: PASS (comprehensive security measures documented)
  - Edge Cases: PASS (10+ edge cases identified and addressed)
- Prompt variant (if applicable): Standard /sp.specify workflow with detailed user requirements
- Next experiment (smallest change to try):
  1. Validate Better Auth integration complexity by reviewing official docs
  2. Prototype email verification flow in isolation before full implementation
  3. Consider if profile data should use JSONB for flexibility vs structured columns
