# Feature Specification: Authentication, Onboarding, and Email Verification System

**Feature Branch**: `004-auth-onboarding-email-verification`
**Created**: 2025-11-29
**Status**: Draft
**Input**: User description: "Physical AI Learning Platform — Authentication, Onboarding, and Email Verification System"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - New User Registration with Email Verification (Priority: P1)

A new learner discovers the Physical AI platform and wants to create an account to access learning content. They sign up with email/password, complete their profile with robotics background information, verify their email address, and gain access to the platform.

**Why this priority**: This is the fundamental entry point for all users. Without the ability to create and verify accounts, no other platform functionality is accessible. This is the absolute minimum viable product (MVP) that enables user access.

**Independent Test**: Can be fully tested by navigating to /signup, creating an account with email/password, filling out the onboarding form with robotics experience data, clicking the verification link in the email, and logging in successfully. Delivers immediate value by allowing users to create verified accounts.

**Acceptance Scenarios**:

1. **Given** a visitor on the signup page, **When** they enter valid email, password, and profile information (robotics/programming experience, AI/ML experience, learning goals), **Then** their account is created in pending state, profile data is stored, and a verification email is sent
2. **Given** a user with unverified account, **When** they click the verification link in their email, **Then** their account is activated, email_verified flag is set to true, and they can log in
3. **Given** a verified user on the login page, **When** they enter correct credentials, **Then** a secure session is created via HTTP-only cookie and they are redirected to the platform
4. **Given** an unverified user attempting to log in, **When** they enter credentials, **Then** login is denied with a message to verify their email first

---

### User Story 2 - Google SSO Registration and Onboarding (Priority: P2)

A new learner prefers to use their existing Google account rather than creating a new password. They click "Sign in with Google", authorize the platform, complete their learning profile, and immediately access the platform (Google accounts are pre-verified).

**Why this priority**: Reduces friction for users who prefer SSO and improves security by leveraging Google's authentication. This is a significant UX improvement but not critical for MVP since email/password authentication is functional.

**Independent Test**: Can be tested independently by clicking "Sign in with Google" on signup page, completing OAuth flow, filling onboarding form, and accessing platform. Works completely independently from email/password flow.

**Acceptance Scenarios**:

1. **Given** a visitor on the signup page, **When** they click "Sign in with Google" and authorize the app, **Then** their account is created with email from Google profile and email_verified is automatically true
2. **Given** a new Google SSO user, **When** they complete OAuth, **Then** they are directed to onboarding form to provide robotics/AI experience and learning goals
3. **Given** a returning Google SSO user, **When** they click "Sign in with Google", **Then** they are authenticated and redirected to platform without onboarding

---

### User Story 3 - Session Management and Protected Resources (Priority: P1)

An authenticated user accesses protected content across the platform. Their session persists across page refreshes, API calls include their session token automatically, and they can log out to invalidate their session.

**Why this priority**: Essential for maintaining user authentication state and protecting content. Without this, users would need to re-authenticate on every page load. Critical security requirement.

**Independent Test**: Can be tested by logging in, navigating to protected pages, refreshing browser, making API calls to /me endpoint, and logging out. Delivers value by maintaining authenticated state.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they navigate to protected pages or refresh the browser, **Then** their session persists via secure HTTP-only cookie
2. **Given** an authenticated user, **When** they make API requests to protected endpoints, **Then** the session cookie is automatically included and validated server-side
3. **Given** an authenticated user, **When** they click logout, **Then** their session is invalidated server-side and client-side, and they are redirected to homepage
4. **Given** an unauthenticated user, **When** they attempt to access protected endpoints, **Then** they receive 401 Unauthorized and are redirected to login

---

### User Story 4 - Profile Data Management and Personalization (Priority: P3)

An authenticated user can view and update their learning profile (robotics experience, AI/ML background, learning goals) to enable personalized content recommendations and learning paths.

**Why this priority**: Enables future personalization features but not critical for initial account access. Can be implemented after core authentication is working.

**Independent Test**: Can be tested by logging in, navigating to /profile, viewing current profile data, updating fields, and saving changes. Works independently and doesn't block other features.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the profile page, **When** they request /profile, **Then** they see their stored robotics/programming experience, AI/ML experience, and learning goals
2. **Given** an authenticated user, **When** they update their profile fields and submit, **Then** the profile record is updated in the database
3. **Given** the platform (future feature), **When** rendering content recommendations, **Then** it can access user profile data to personalize the experience

---

### User Story 5 - Email Verification Expiration and Resend (Priority: P3)

A user's verification email expires after 24 hours. They can request a new verification email if needed, ensuring security while providing recovery path.

**Why this priority**: Important security feature but not critical for happy path. Most users verify immediately. Can be added after core flow works.

**Independent Test**: Can be tested by creating account, waiting for code expiration, attempting to verify with expired code (gets error), requesting new verification email, and verifying with new code.

**Acceptance Scenarios**:

1. **Given** a verification code older than 24 hours, **When** user clicks verification link, **Then** they receive error message and option to resend verification email
2. **Given** a user requesting new verification email, **When** they click resend, **Then** old codes are invalidated and new verification email is sent
3. **Given** multiple verification codes for same user, **When** user verifies with latest code, **Then** account is activated and all codes are marked as used

---

### Edge Cases

- What happens when a user tries to register with an email that's already registered?
  - System returns error: "Email already registered. Please log in or reset password."
- What happens when a user clicks an expired verification link?
  - System displays error page with option to resend verification email
- What happens when a user tries to register with Google using email that already exists via email/password?
  - System recognizes existing account and links Google SSO to existing account (requires email verification match)
- What happens when verification email fails to send (email service down)?
  - Account is created but flagged for retry; admin notification; user shown message to contact support
- What happens when session cookie expires during active use?
  - User receives 401 on next API call and is redirected to login with message "Session expired, please log in again"
- What happens when user attempts SQL injection or XSS in profile fields?
  - Pydantic validation rejects invalid input; prepared statements prevent SQL injection; output is HTML-escaped
- What happens when user loses verification email?
  - Provide "Resend verification email" button on login page for unverified accounts
- What happens when multiple tabs/devices are logged in simultaneously?
  - All sessions are valid until explicitly logged out; logout in one location doesn't invalidate other sessions (configurable)

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Account Management

- **FR-001**: System MUST allow users to register with email and password
- **FR-002**: System MUST allow users to register/login via Google SSO using Better Auth
- **FR-003**: System MUST validate email format during registration
- **FR-004**: System MUST enforce password requirements: minimum 8 characters, at least one uppercase, one lowercase, one number
- **FR-005**: System MUST hash and salt passwords using Better Auth's built-in security (bcrypt or argon2)
- **FR-006**: System MUST create user record in `users` table with Better Auth ID reference
- **FR-007**: System MUST prevent duplicate email registration (return clear error message)
- **FR-008**: System MUST create session token and set as secure HTTP-only cookie on successful login
- **FR-009**: System MUST validate session token on all protected endpoint requests via dependency injection
- **FR-010**: System MUST invalidate session server-side on logout

#### Email Verification

- **FR-011**: System MUST generate unique verification code (UUID or secure random string) on account creation
- **FR-012**: System MUST store verification code in `email_verification` table with user ID, code, and expiration timestamp (24 hours)
- **FR-013**: System MUST send verification email containing clickable link with embedded code
- **FR-014**: System MUST provide verification endpoint `/verify-email?code={code}` that validates code and activates account
- **FR-015**: System MUST set `email_verified` flag to true in users table upon successful verification
- **FR-016**: System MUST reject login attempts for unverified email/password accounts
- **FR-017**: System MUST automatically mark Google SSO accounts as verified (email_verified = true)
- **FR-018**: System MUST expire verification codes after 24 hours
- **FR-019**: System MUST allow users to request new verification email (invalidating previous codes)

#### Onboarding & Profile Management

- **FR-020**: System MUST present onboarding form after successful registration (before or after verification based on UX decision)
- **FR-021**: System MUST capture structured profile data:
  - Robotics/Programming Experience: dropdown or radio (None, Beginner, Intermediate, Advanced, Expert)
  - AI/ML Experience: dropdown or radio (None, Beginner, Intermediate, Advanced, Expert)
  - Learning Goals: multi-select checkboxes or text area (e.g., "Build humanoid robot", "Understand AI fundamentals", "Career transition", "Academic research")
- **FR-022**: System MUST store profile data in `profiles` table linked to user ID
- **FR-023**: System MUST provide `/profile` endpoint (GET) to retrieve authenticated user's profile
- **FR-024**: System MUST provide `/profile` endpoint (PUT/PATCH) to update authenticated user's profile
- **FR-025**: System MUST validate profile data with Pydantic models (required fields, valid enum values)

#### Session Management

- **FR-026**: System MUST use secure HTTP-only cookies for session tokens (prevent XSS)
- **FR-027**: System MUST set SameSite=Lax or Strict on session cookies (prevent CSRF)
- **FR-028**: System MUST set Secure flag on cookies in production (HTTPS only)
- **FR-029**: System MUST provide `/me` endpoint returning current authenticated user's data (id, email, name, email_verified)
- **FR-030**: System MUST use dependency injection to protect endpoints requiring authentication
- **FR-031**: System MUST return 401 Unauthorized for invalid or missing session tokens

#### Frontend Integration

- **FR-032**: Docusaurus frontend MUST provide custom React page for Signup (`/signup`)
- **FR-033**: Docusaurus frontend MUST provide custom React page for Login (`/login`)
- **FR-034**: Docusaurus frontend MUST provide custom React page for Email Verification result (`/verify-email`)
- **FR-035**: Docusaurus frontend MUST provide custom React page/component for Onboarding form
- **FR-036**: Frontend MUST integrate Google SSO button using Better Auth client SDK
- **FR-037**: Frontend MUST implement session check hook (useAuth or similar) to determine logged-in state
- **FR-038**: Frontend MUST display user info in navbar when authenticated (e.g., email or name + logout button)
- **FR-039**: Frontend MUST redirect unauthenticated users to `/login` when accessing protected pages
- **FR-040**: Frontend MUST display loading state during authentication checks and API calls

### Key Entities

- **User**: Represents a platform user account
  - Attributes: id (PK), email (unique), name, better_auth_id (FK to Better Auth), email_verified (boolean), created_at, updated_at
  - Relationships: One-to-One with Profile, One-to-Many with EmailVerification

- **Profile**: Stores structured user learning background and goals
  - Attributes: id (PK), user_id (FK to User, unique), robotics_programming_experience (enum), ai_ml_experience (enum), learning_goals (text or JSON), created_at, updated_at
  - Relationships: Belongs to User

- **EmailVerification**: Stores verification codes and expiration
  - Attributes: id (PK), user_id (FK to User), code (unique), expires_at (timestamp), verified_at (timestamp, nullable), created_at
  - Relationships: Belongs to User

- **Session**: Managed by Better Auth (abstracted)
  - Better Auth handles session storage, token generation, and validation
  - Sessions link to user via Better Auth's internal schema

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration (including onboarding) in under 3 minutes
- **SC-002**: Email verification link works on first click with >99% success rate
- **SC-003**: Authenticated sessions persist for configured duration (e.g., 7 days) without re-authentication
- **SC-004**: Login requests complete in <500ms (excluding external Google OAuth latency)
- **SC-005**: System handles at least 100 concurrent users without session or login degradation
- **SC-006**: Zero unhandled authentication errors in production (all errors return appropriate status codes and messages)
- **SC-007**: 95% of users successfully verify email within 24 hours of registration
- **SC-008**: Frontend authentication state updates within 200ms of login/logout actions
- **SC-009**: All authentication endpoints return standardized JSON responses with clear error messages
- **SC-010**: Profile data is correctly stored for >99% of onboarding form submissions

## Technical Specification

### Architecture Overview

**Stack**:
- **Backend**: FastAPI 3.13 with Better Auth
- **Database**: Neon Serverless PostgreSQL
- **Frontend**: Docusaurus 3.9.2 (React) with custom authentication pages
- **Email Service**: [NEEDS CLARIFICATION: SendGrid, AWS SES, SMTP, or other?]
- **Session Storage**: HTTP-only cookies with Better Auth token management

**Key Design Decisions**:
1. Better Auth provides authentication layer (not reinventing auth primitives)
2. Email verification required for email/password accounts, auto-verified for Google SSO
3. Onboarding form presented after account creation (can be skipped and completed later from profile page)
4. Secure session tokens stored in HTTP-only cookies (not localStorage to prevent XSS)
5. Dependency injection for protected endpoints (centralizes auth logic)

---

### Database Schema

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    better_auth_id VARCHAR(255) UNIQUE NOT NULL,  -- References Better Auth user ID
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_better_auth_id ON users(better_auth_id);
```

#### Profiles Table
```sql
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    robotics_programming_experience VARCHAR(50) CHECK (robotics_programming_experience IN ('none', 'beginner', 'intermediate', 'advanced', 'expert')),
    ai_ml_experience VARCHAR(50) CHECK (ai_ml_experience IN ('none', 'beginner', 'intermediate', 'advanced', 'expert')),
    learning_goals TEXT,  -- JSON array or comma-separated text
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_profiles_user_id ON profiles(user_id);
```

#### Email Verification Table
```sql
CREATE TABLE email_verification (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    code VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_email_verification_code ON email_verification(code);
CREATE INDEX idx_email_verification_user_id ON email_verification(user_id);
CREATE INDEX idx_email_verification_expires_at ON email_verification(expires_at);
```

**Migration Notes**:
- Use Alembic or similar migration tool for schema versioning
- Better Auth may create its own tables (sessions, oauth_accounts, etc.) — these are managed by Better Auth

---

### API Endpoints

#### POST /api/auth/signup
**Description**: Register new user with email/password

**Request Body** (Pydantic model):
```python
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str
```

**Response** (Success 201):
```json
{
    "user_id": 123,
    "email": "user@example.com",
    "email_verified": false,
    "message": "Account created. Please check your email to verify your account."
}
```

**Response** (Error 400):
```json
{
    "detail": "Email already registered"
}
```

**Logic**:
1. Validate email and password with Pydantic
2. Check if email already exists → 400 if duplicate
3. Create user via Better Auth (hashes password)
4. Store user record in `users` table with Better Auth ID
5. Generate verification code (UUID)
6. Store code in `email_verification` with 24-hour expiration
7. Send verification email
8. Return user data

---

#### POST /api/auth/google
**Description**: Authenticate via Google SSO (Better Auth handles OAuth flow)

**Better Auth Integration**: Better Auth provides this endpoint automatically

**Response** (Success 200):
```json
{
    "user_id": 124,
    "email": "user@gmail.com",
    "email_verified": true,
    "message": "Logged in successfully via Google"
}
```

**Logic**:
1. Better Auth handles OAuth redirect and token exchange
2. Create or retrieve user record linked to Google account
3. Set email_verified = true (Google emails are verified)
4. Create session and set HTTP-only cookie
5. Redirect to onboarding if first login, else to dashboard

---

#### POST /api/auth/login
**Description**: Login with email/password

**Request Body**:
```python
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

**Response** (Success 200):
```json
{
    "user_id": 123,
    "email": "user@example.com",
    "email_verified": true
}
```

**Response** (Error 401):
```json
{
    "detail": "Invalid credentials"
}
```

**Response** (Error 403):
```json
{
    "detail": "Email not verified. Please check your email."
}
```

**Logic**:
1. Validate credentials via Better Auth
2. Check email_verified flag → 403 if false
3. Create session and set HTTP-only cookie
4. Return user data

---

#### POST /api/auth/logout
**Description**: Invalidate current session

**Response** (Success 200):
```json
{
    "message": "Logged out successfully"
}
```

**Logic**:
1. Extract session token from cookie
2. Invalidate session in Better Auth
3. Clear session cookie (set Max-Age=0)
4. Return success

---

#### GET /api/auth/verify-email?code={code}
**Description**: Verify email address with verification code

**Query Parameters**:
- `code`: Verification code (UUID string)

**Response** (Success 200):
```json
{
    "message": "Email verified successfully. You can now log in."
}
```

**Response** (Error 400):
```json
{
    "detail": "Invalid or expired verification code"
}
```

**Logic**:
1. Query `email_verification` for code
2. Check if code exists and not expired (expires_at > now)
3. If valid, set users.email_verified = true
4. Set verified_at = now in email_verification record
5. Return success
6. If invalid/expired, return 400 with clear message

---

#### GET /api/auth/me
**Description**: Get current authenticated user info

**Headers**: Cookie with session token (automatic)

**Response** (Success 200):
```json
{
    "id": 123,
    "email": "user@example.com",
    "name": "John Doe",
    "email_verified": true
}
```

**Response** (Error 401):
```json
{
    "detail": "Not authenticated"
}
```

**Logic**:
1. Dependency injection validates session token
2. If valid, retrieve user from database
3. Return user data
4. If invalid/missing, return 401

---

#### GET /api/profile
**Description**: Get authenticated user's profile

**Response** (Success 200):
```json
{
    "user_id": 123,
    "robotics_programming_experience": "intermediate",
    "ai_ml_experience": "beginner",
    "learning_goals": "Build humanoid robot, Understand AI fundamentals"
}
```

**Response** (Error 404):
```json
{
    "detail": "Profile not found"
}
```

**Logic**:
1. Authenticate user via dependency injection
2. Query `profiles` table by user_id
3. Return profile data or 404 if not created yet

---

#### POST /api/profile
**Description**: Create or update authenticated user's profile

**Request Body**:
```python
class ProfileRequest(BaseModel):
    robotics_programming_experience: Literal['none', 'beginner', 'intermediate', 'advanced', 'expert']
    ai_ml_experience: Literal['none', 'beginner', 'intermediate', 'advanced', 'expert']
    learning_goals: str
```

**Response** (Success 200):
```json
{
    "message": "Profile updated successfully",
    "profile": {
        "robotics_programming_experience": "intermediate",
        "ai_ml_experience": "beginner",
        "learning_goals": "Build humanoid robot"
    }
}
```

**Logic**:
1. Authenticate user via dependency injection
2. Validate request body with Pydantic
3. Upsert profile record (INSERT ... ON CONFLICT UPDATE)
4. Return updated profile

---

#### POST /api/auth/resend-verification
**Description**: Resend verification email for unverified accounts

**Request Body**:
```python
class ResendVerificationRequest(BaseModel):
    email: EmailStr
```

**Response** (Success 200):
```json
{
    "message": "Verification email sent. Please check your inbox."
}
```

**Response** (Error 400):
```json
{
    "detail": "Email already verified or account not found"
}
```

**Logic**:
1. Check if user exists and email is unverified
2. Invalidate previous verification codes
3. Generate new code and expiration
4. Send verification email
5. Return success

---

### Frontend Pages & Components

#### 1. Signup Page (`/signup`)
**Location**: `book-source/src/pages/signup.tsx`

**Components**:
- Email/password input form
- "Sign up with Google" button
- Link to Login page
- Form validation (client-side + server-side errors)

**Behavior**:
1. User fills email, password, name
2. On submit, POST to `/api/auth/signup`
3. On success, show message "Check your email to verify account" and redirect to login
4. On Google button click, redirect to Better Auth Google OAuth flow
5. Display validation errors inline

---

#### 2. Login Page (`/login`)
**Location**: `book-source/src/pages/login.tsx`

**Components**:
- Email/password input form
- "Sign in with Google" button
- Link to Signup page
- "Resend verification email" button (if unverified error occurs)

**Behavior**:
1. User fills email, password
2. On submit, POST to `/api/auth/login`
3. On success, redirect to dashboard or homepage
4. On 403 (unverified), show "Resend verification email" button
5. On 401, show "Invalid credentials" error

---

#### 3. Email Verification Page (`/verify-email`)
**Location**: `book-source/src/pages/verify-email.tsx`

**Behavior**:
1. Extract `code` from URL query params
2. On mount, send GET to `/api/auth/verify-email?code={code}`
3. On success, show "Email verified! You can now log in" and redirect to login after 3 seconds
4. On error, show "Invalid or expired code" with "Resend verification email" button

---

#### 4. Onboarding Form (`/onboarding`)
**Location**: `book-source/src/pages/onboarding.tsx`

**Components**:
- Dropdown/radio for robotics/programming experience
- Dropdown/radio for AI/ML experience
- Text area or checkboxes for learning goals
- Submit button

**Behavior**:
1. Displayed after successful signup or first Google login
2. On submit, POST to `/api/profile`
3. On success, redirect to dashboard or homepage
4. "Skip for now" button saves empty/default values and redirects

---

#### 5. Profile Page (`/profile`)
**Location**: `book-source/src/pages/profile.tsx`

**Components**:
- Display current profile data (read-only sections)
- Edit form (same fields as onboarding)
- Save button

**Behavior**:
1. On mount, GET from `/api/profile`
2. Display data or "Complete your profile" if 404
3. User edits fields
4. On save, POST to `/api/profile`
5. Show success message

---

#### 6. Authentication Hook (`useAuth`)
**Location**: `book-source/src/hooks/useAuth.ts`

**Purpose**: Centralized hook for checking authentication state

**API**:
```typescript
const { user, loading, isAuthenticated, logout } = useAuth();
```

**Behavior**:
1. On mount, call GET `/api/auth/me`
2. If 200, set user data and isAuthenticated = true
3. If 401, set isAuthenticated = false
4. Provide logout function that calls POST `/api/auth/logout` and clears state
5. Show loading state during initial check

---

#### 7. Protected Route Component
**Location**: `book-source/src/components/ProtectedRoute.tsx`

**Usage**:
```tsx
<ProtectedRoute>
  <ProfilePage />
</ProtectedRoute>
```

**Behavior**:
1. Uses `useAuth()` hook
2. If loading, show spinner
3. If not authenticated, redirect to `/login`
4. If authenticated, render children

---

### Email Templates

#### Verification Email
**Subject**: Verify your email for Physical AI Learning Platform

**Body** (HTML):
```html
<h1>Welcome to Physical AI Learning Platform!</h1>
<p>Hi {{name}},</p>
<p>Thank you for creating an account. Please verify your email address by clicking the link below:</p>
<a href="{{verification_link}}">Verify Email</a>
<p>This link will expire in 24 hours.</p>
<p>If you didn't create this account, please ignore this email.</p>
```

**Variables**:
- `{{name}}`: User's name
- `{{verification_link}}`: `https://yourdomain.com/verify-email?code={code}`

**Service**: [NEEDS CLARIFICATION: SendGrid, AWS SES, or SMTP server?]

---

### Security Considerations

1. **Password Security**:
   - Better Auth handles hashing (bcrypt or argon2)
   - Enforce strong password requirements client and server-side
   - Never log or expose passwords

2. **Session Security**:
   - HTTP-only cookies prevent XSS attacks
   - SameSite=Lax/Strict prevents CSRF
   - Secure flag ensures HTTPS-only in production
   - Session expiration configurable (default 7 days)

3. **Email Verification**:
   - Codes expire after 24 hours
   - Codes are UUIDs (128-bit random, collision-resistant)
   - Codes stored hashed in database (optional extra security)

4. **Input Validation**:
   - Pydantic models validate all inputs
   - Email format validation via EmailStr
   - Password complexity enforced
   - Profile data constrained to enum values

5. **SQL Injection Prevention**:
   - Use parameterized queries (SQLAlchemy ORM or prepared statements)
   - Never concatenate user input into SQL

6. **XSS Prevention**:
   - React escapes output by default
   - Sanitize any user-generated content before rendering
   - Avoid dangerouslySetInnerHTML

7. **Rate Limiting** [NEEDS CLARIFICATION: Should we implement rate limiting on login/signup?]:
   - Consider rate limiting login attempts (e.g., 5 attempts per 15 minutes)
   - Rate limit verification email resend (e.g., 3 requests per hour)

8. **CORS Configuration**:
   - Configure CORS to allow requests from Docusaurus domain only
   - Example: allow `https://yourdomain.com` in production

---

### Deployment & Configuration

#### Environment Variables

**Backend (.env)**:
```env
DATABASE_URL=postgresql://user:password@neon-host/dbname
BETTER_AUTH_SECRET=random-secret-key-min-32-chars
BETTER_AUTH_GOOGLE_CLIENT_ID=google-oauth-client-id
BETTER_AUTH_GOOGLE_CLIENT_SECRET=google-oauth-client-secret
EMAIL_SERVICE_API_KEY=sendgrid-api-key-or-similar
EMAIL_FROM_ADDRESS=noreply@yourdomain.com
FRONTEND_URL=https://yourdomain.com
SESSION_COOKIE_DOMAIN=yourdomain.com
SESSION_MAX_AGE=604800  # 7 days in seconds
```

**Frontend (.env)**:
```env
REACT_APP_API_URL=https://api.yourdomain.com
REACT_APP_GOOGLE_CLIENT_ID=google-oauth-client-id
```

#### Deployment Steps

1. **Database Setup**:
   - Provision Neon Serverless PostgreSQL instance
   - Run migrations to create tables
   - Set up Better Auth schema

2. **Backend Deployment**:
   - Deploy FastAPI to serverless platform (e.g., AWS Lambda, Vercel, Railway)
   - Set environment variables
   - Configure CORS for frontend domain

3. **Frontend Deployment**:
   - Build Docusaurus: `npm run build`
   - Deploy static files to CDN (Netlify, Vercel, GitHub Pages)
   - Configure environment variables

4. **Email Service Setup**:
   - Configure SendGrid/SES with verified sender domain
   - Create email templates
   - Test email delivery

5. **Google OAuth Setup**:
   - Create Google Cloud project
   - Enable Google+ API
   - Configure OAuth consent screen
   - Create OAuth credentials (client ID and secret)
   - Add authorized redirect URIs

---

### Testing Strategy

#### Unit Tests (Backend)

**Tools**: pytest, pytest-asyncio

**Test Cases**:
- [ ] Signup with valid email/password creates user and sends verification email
- [ ] Signup with duplicate email returns 400 error
- [ ] Login with unverified account returns 403 error
- [ ] Login with verified account creates session
- [ ] Email verification with valid code sets email_verified to true
- [ ] Email verification with expired code returns 400 error
- [ ] Protected endpoints return 401 without valid session
- [ ] Protected endpoints return user data with valid session
- [ ] Profile creation stores data correctly
- [ ] Profile update modifies existing record

#### Integration Tests (Backend + Database)

**Test Cases**:
- [ ] Full signup → verify → login flow completes successfully
- [ ] Google SSO flow creates user with email_verified = true
- [ ] Session persists across requests
- [ ] Logout invalidates session
- [ ] Resend verification email invalidates old codes

#### Frontend Tests

**Tools**: Jest, React Testing Library

**Test Cases**:
- [ ] Signup form validates email format
- [ ] Signup form validates password requirements
- [ ] Login form displays error on invalid credentials
- [ ] useAuth hook sets user state on successful /me call
- [ ] useAuth hook redirects to login on 401
- [ ] Onboarding form submits data to /api/profile
- [ ] Protected routes redirect unauthenticated users

#### End-to-End Tests

**Tools**: Playwright or Cypress

**Test Cases**:
- [ ] User completes full signup → verify → login → onboarding flow
- [ ] User logs in with Google SSO and completes onboarding
- [ ] User logs out and session is cleared
- [ ] User navigates to protected page and is redirected to login

---

### Open Questions & Clarifications Needed

1. **Email Service**: Which email service should we use? (SendGrid, AWS SES, SMTP server, other?)
   - **Impact**: Configuration, API integration, cost
   - **Recommendation**: SendGrid for ease of use, or AWS SES for cost efficiency

2. **Rate Limiting**: Should we implement rate limiting on login/signup endpoints?
   - **Impact**: Security vs. complexity
   - **Recommendation**: Yes, use FastAPI-Limiter or similar (5 login attempts per 15 minutes)

3. **Session Duration**: How long should sessions last? (Default 7 days, configurable?)
   - **Impact**: User experience vs. security
   - **Recommendation**: 7 days with "Remember me" checkbox (30 days if checked)

4. **Onboarding Flow**: Should onboarding be mandatory before accessing content, or skippable?
   - **Impact**: User friction vs. data collection
   - **Recommendation**: Skippable with persistent prompt in navbar ("Complete your profile")

5. **Password Reset**: Not mentioned in original spec — should we include password reset flow?
   - **Impact**: Additional endpoints, email templates, database schema
   - **Recommendation**: Yes, critical for production (add to spec if approved)

6. **Multi-Factor Authentication (MFA)**: Should we support MFA (TOTP, SMS)?
   - **Impact**: Security vs. complexity
   - **Recommendation**: Not for MVP, add later if needed

7. **Account Linking**: If user signs up with email/password then later uses Google with same email, should we link accounts?
   - **Impact**: User experience, complexity
   - **Recommendation**: Yes, link accounts automatically if email matches and is verified

8. **Learning Goals Format**: Should learning goals be free text, predefined checkboxes, or both?
   - **Impact**: Data structure, personalization capability
   - **Recommendation**: Multi-select checkboxes with "Other (specify)" text field

9. **Profile Visibility**: Are profiles private or can other users see them? (For future community features)
   - **Impact**: Privacy settings, data model
   - **Recommendation**: Private for MVP, add visibility settings later

10. **Neon PostgreSQL Configuration**: Do we need connection pooling or read replicas?
    - **Impact**: Performance, cost
    - **Recommendation**: Neon handles pooling; start with single instance

---

### Dependencies & Prerequisites

**External Dependencies**:
- FastAPI 3.13+
- Better Auth (latest stable)
- Neon Serverless PostgreSQL
- Email service (SendGrid or AWS SES)
- Google OAuth credentials
- Pydantic 2.x
- SQLAlchemy 2.x (or asyncpg for async queries)
- React 18+ (provided by Docusaurus)
- TypeScript 5.x

**Internal Dependencies**:
- Docusaurus site structure (already implemented)
- Project constitution (`.specify/memory/constitution.md`)
- Git repository and version control
- Development environment with Node 18+ and Python 3.11+

---

### Success Metrics (Detailed)

**Functional Metrics**:
- [ ] 100% of valid signups receive verification email within 10 seconds
- [ ] 100% of verification links work on first click (unless expired)
- [ ] Login success rate >99% for valid credentials
- [ ] Session persistence across page refreshes and browser restarts (until expiration)
- [ ] Profile data accuracy: 100% of submitted profiles stored correctly

**Performance Metrics**:
- [ ] Signup endpoint response time: <1 second (excluding email send)
- [ ] Login endpoint response time: <500ms
- [ ] /me endpoint response time: <200ms
- [ ] Email delivery time: <30 seconds to inbox
- [ ] Frontend auth state update: <200ms after login/logout

**Security Metrics**:
- [ ] Zero plain-text password storage
- [ ] Zero XSS vulnerabilities (all output escaped)
- [ ] Zero SQL injection vulnerabilities (parameterized queries)
- [ ] 100% of sessions use HTTP-only secure cookies
- [ ] 100% of verification codes expire after 24 hours

**User Experience Metrics**:
- [ ] 90% of users complete signup→verification→login in one session
- [ ] <5% of users request verification email resend
- [ ] Average time to complete onboarding: <2 minutes
- [ ] <1% of users abandon signup due to errors

---

### Risks & Mitigations

#### Risk 1: Email Deliverability Issues
**Impact**: Users can't verify accounts, blocking access
**Likelihood**: Medium
**Mitigation**:
- Use reputable email service (SendGrid/AWS SES)
- Implement email delivery monitoring and alerts
- Provide "Resend verification email" option
- Consider SMS verification as backup (future)

#### Risk 2: Better Auth Integration Complexity
**Impact**: Authentication logic breaks or is insecure
**Likelihood**: Low (Better Auth is mature)
**Mitigation**:
- Follow Better Auth documentation closely
- Use official examples and templates
- Test auth flows thoroughly
- Have fallback plan (implement JWT manually if needed)

#### Risk 3: Google OAuth Configuration Errors
**Impact**: Google SSO doesn't work
**Likelihood**: Medium (common misconfiguration)
**Mitigation**:
- Test OAuth flow in development environment first
- Verify redirect URIs match exactly
- Check OAuth consent screen configuration
- Provide clear error messages for users

#### Risk 4: Session Hijacking / XSS Attacks
**Impact**: Unauthorized access to accounts
**Likelihood**: Low (with HTTP-only cookies)
**Mitigation**:
- Use HTTP-only, Secure, SameSite cookies
- Implement CSRF protection
- Sanitize all user input
- Regular security audits

#### Risk 5: Database Connection Issues with Neon
**Impact**: Auth endpoints fail, users can't log in
**Likelihood**: Low (Neon is reliable)
**Mitigation**:
- Implement connection retry logic
- Monitor database health
- Use connection pooling
- Have database failover plan

#### Risk 6: Profile Data Schema Changes
**Impact**: Need to migrate existing profiles
**Likelihood**: Medium (requirements evolve)
**Mitigation**:
- Use database migrations (Alembic)
- Design schema with flexibility (JSONB for learning_goals)
- Version API responses
- Plan for backward compatibility

---

### Future Enhancements (Out of Scope for MVP)

1. **Password Reset Flow**: Forgot password → email link → reset password
2. **Multi-Factor Authentication (MFA)**: TOTP, SMS codes
3. **Social Login Expansion**: GitHub, Microsoft, Facebook OAuth
4. **Profile Enrichment**: Avatar upload, bio, location, interests
5. **Account Deletion**: GDPR-compliant self-service account deletion
6. **Admin Panel**: Manage users, view metrics, moderate content
7. **Activity Logging**: Track login history, IP addresses, devices
8. **Email Preferences**: Unsubscribe from marketing emails, notification settings
9. **Account Linking**: Link multiple OAuth providers to one account
10. **Progressive Profiling**: Collect more profile data over time (not all at signup)

---

## Approval and Sign-Off

**Prepared By**: Claude Code (AI Assistant)
**Date**: 2025-11-29
**Status**: Draft — Awaiting User Approval

**Next Steps**:
1. **User reviews specification and provides clarifications** (especially open questions)
2. **Specification approved** → Proceed to planning phase (`/sp.plan`)
3. **Generate tasks** → Detailed implementation tasks (`/sp.tasks`)
4. **Begin implementation** → Build backend, frontend, database

**Approval Checklist**:
- [ ] User approves overall architecture and tech stack
- [ ] User clarifies open questions (email service, rate limiting, etc.)
- [ ] User confirms database schema design
- [ ] User approves API endpoint contracts
- [ ] User confirms frontend page structure
- [ ] User approves security measures
- [ ] Ready to proceed to planning phase

---

**END OF SPECIFICATION**
