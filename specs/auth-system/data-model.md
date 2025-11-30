# Data Model: Authentication System

**Feature**: Authentication, Onboarding, and Email Verification
**Date**: 2025-11-29
**Database**: Neon Serverless PostgreSQL
**ORM**: SQLAlchemy 2.0 (async)
**Framework**: FastAPI-Users

---

## Overview

The authentication system uses **four core entities** to manage user accounts, sessions, profiles, and email verification:

1. **User** — Base authentication entity (managed by FastAPI-Users)
2. **OAuthAccount** — OAuth provider linkage (Google SSO)
3. **Profile** — User learning background and goals
4. **EmailVerification** — Email verification tokens and expiration

**Design Principles**:
- Normalized schema (3NF)
- Foreign key constraints with cascade delete
- Indexes on all lookup columns
- Enum constraints for experience levels
- Timestamps for audit trail

---

## Entity Relationship Diagram

```
┌──────────────────┐
│      User        │
│==================│
│ id (UUID) PK     │
│ email            │◄─────────┐
│ hashed_password  │          │
│ is_active        │          │
│ is_superuser     │          │
│ is_verified      │          │
│ created_at       │          │
│ updated_at       │          │
└──────────────────┘          │
         │                     │
         │ 1:1                 │ 1:N
         ▼                     │
┌──────────────────┐          │
│     Profile      │          │
│==================│          │
│ id (int) PK      │          │
│ user_id (UUID)FK │──────────┘
│ robotics_exp     │
│ ai_ml_exp        │
│ learning_goals   │
│ created_at       │
│ updated_at       │
└──────────────────┘

         │
         │ 1:N
         ▼
┌──────────────────┐
│ OAuthAccount     │
│==================│
│ id (UUID) PK     │
│ user_id (UUID)FK │
│ oauth_name       │  (e.g., "google")
│ access_token     │
│ expires_at       │
│ refresh_token    │
│ account_id       │  (Google user ID)
│ account_email    │
└──────────────────┘

         │
         │ 1:N
         ▼
┌──────────────────┐
│EmailVerification │
│==================│
│ id (int) PK      │
│ user_id (UUID)FK │
│ token (UUID)     │
│ expires_at       │
│ created_at       │
└──────────────────┘
```

---

## Entity Definitions

### 1. User Entity

**Purpose**: Core authentication entity managed by FastAPI-Users

**Table Name**: `user` (FastAPI-Users convention)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | User unique identifier |
| `email` | VARCHAR(320) | UNIQUE NOT NULL | User email address (RFC 5321 max length) |
| `hashed_password` | VARCHAR(1024) | NOT NULL | Bcrypt hashed password |
| `is_active` | BOOLEAN | NOT NULL DEFAULT TRUE | Account active status |
| `is_superuser` | BOOLEAN | NOT NULL DEFAULT FALSE | Admin privileges flag |
| `is_verified` | BOOLEAN | NOT NULL DEFAULT FALSE | Email verification status |
| `created_at` | TIMESTAMP | NOT NULL DEFAULT NOW() | Account creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `PRIMARY KEY (id)`
- `UNIQUE INDEX idx_user_email ON user(email)`

**Relationships**:
- One-to-One with `Profile` (user_id FK)
- One-to-Many with `OAuthAccount` (user_id FK)
- One-to-Many with `EmailVerification` (user_id FK)

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Password minimum 8 characters (enforced before hashing)
- Email must be unique across system

**State Transitions**:
```
CREATED (is_verified=false, is_active=true)
   │
   ├─► EMAIL_VERIFIED (is_verified=true)
   │
   ├─► DEACTIVATED (is_active=false)
   │
   └─► DELETED (soft delete or hard delete)
```

**SQLAlchemy Model**:
```python
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String, Boolean, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    # Inherited from SQLAlchemyBaseUserTableUUID:
    # id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    # hashed_password: Mapped[str] = mapped_column(String(1024), nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    # is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    profile: Mapped["Profile"] = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    oauth_accounts: Mapped[list["OAuthAccount"]] = relationship("OAuthAccount", back_populates="user", cascade="all, delete-orphan")
    email_verifications: Mapped[list["EmailVerification"]] = relationship("EmailVerification", back_populates="user", cascade="all, delete-orphan")
```

---

### 2. OAuthAccount Entity

**Purpose**: Store OAuth provider credentials (Google, GitHub, etc.)

**Table Name**: `oauth_account` (FastAPI-Users convention)

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | OAuth account unique ID |
| `user_id` | UUID | FOREIGN KEY NOT NULL | Reference to user.id |
| `oauth_name` | VARCHAR(100) | NOT NULL | Provider name ("google", "github") |
| `access_token` | TEXT | NOT NULL | OAuth access token |
| `expires_at` | INTEGER | NULLABLE | Token expiration (Unix timestamp) |
| `refresh_token` | TEXT | NULLABLE | OAuth refresh token |
| `account_id` | VARCHAR(320) | NOT NULL | Provider user ID (e.g., Google sub) |
| `account_email` | VARCHAR(320) | NOT NULL | Email from OAuth provider |

**Indexes**:
- `PRIMARY KEY (id)`
- `INDEX idx_oauth_user_id ON oauth_account(user_id)`
- `UNIQUE INDEX idx_oauth_provider ON oauth_account(oauth_name, account_id)`

**Relationships**:
- Belongs to `User` (many-to-one via user_id)

**Validation Rules**:
- `oauth_name` must be in allowed providers: ["google", "github", "facebook"]
- `account_id` + `oauth_name` must be unique (one Google account = one user)
- `account_email` must match `user.email` (enforced in business logic)

**SQLAlchemy Model**:
```python
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    __tablename__ = "oauth_account"

    # Inherited from SQLAlchemyBaseOAuthAccountTableUUID:
    # id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="cascade"), nullable=False)
    # oauth_name: Mapped[str] = mapped_column(String(100), nullable=False)
    # access_token: Mapped[str] = mapped_column(Text, nullable=False)
    # expires_at: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    # account_id: Mapped[str] = mapped_column(String(320), nullable=False)
    # account_email: Mapped[str] = mapped_column(String(320), nullable=False)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="oauth_accounts")
```

---

### 3. Profile Entity

**Purpose**: Store user learning background and goals for personalization

**Table Name**: `profile`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Profile unique ID |
| `user_id` | UUID | FOREIGN KEY UNIQUE NOT NULL | Reference to user.id (one-to-one) |
| `robotics_programming_experience` | VARCHAR(20) | CHECK constraint | Experience level enum |
| `ai_ml_experience` | VARCHAR(20) | CHECK constraint | AI/ML experience enum |
| `learning_goals` | TEXT | NULLABLE | User learning objectives |
| `created_at` | TIMESTAMP | NOT NULL DEFAULT NOW() | Profile creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `PRIMARY KEY (id)`
- `UNIQUE INDEX idx_profile_user_id ON profile(user_id)`

**Relationships**:
- Belongs to `User` (one-to-one via user_id)

**Validation Rules**:
- `robotics_programming_experience` ∈ ["none", "beginner", "intermediate", "advanced", "expert"]
- `ai_ml_experience` ∈ ["none", "beginner", "intermediate", "advanced", "expert"]
- `learning_goals` max length 2000 characters
- `user_id` must reference existing user (foreign key constraint)

**State Transitions**:
```
INCOMPLETE (created during signup, fields may be null)
   │
   ▼
COMPLETE (all required fields filled via onboarding)
   │
   ▼
UPDATED (user modifies profile later)
```

**SQLAlchemy Model**:
```python
from sqlalchemy import Integer, String, Text, TIMESTAMP, ForeignKey, CheckConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
import uuid

class ExperienceLevel(str, enum.Enum):
    """Experience level enumeration"""
    NONE = "none"
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False)

    robotics_programming_experience: Mapped[ExperienceLevel | None] = mapped_column(
        SQLEnum(ExperienceLevel, name="experience_level"),
        nullable=True
    )
    ai_ml_experience: Mapped[ExperienceLevel | None] = mapped_column(
        SQLEnum(ExperienceLevel, name="experience_level"),
        nullable=True
    )
    learning_goals: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="profile")
```

---

### 4. EmailVerification Entity

**Purpose**: Store email verification tokens with expiration

**Table Name**: `email_verification`

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Verification record ID |
| `user_id` | UUID | FOREIGN KEY NOT NULL | Reference to user.id |
| `token` | UUID | UNIQUE NOT NULL | Verification token (UUID v4) |
| `expires_at` | TIMESTAMP | NOT NULL | Token expiration (24 hours) |
| `created_at` | TIMESTAMP | NOT NULL DEFAULT NOW() | Token creation timestamp |

**Indexes**:
- `PRIMARY KEY (id)`
- `UNIQUE INDEX idx_verification_token ON email_verification(token)`
- `INDEX idx_verification_user_id ON email_verification(user_id)`
- `INDEX idx_verification_expires_at ON email_verification(expires_at)` (for cleanup queries)

**Relationships**:
- Belongs to `User` (many-to-one via user_id)

**Validation Rules**:
- `token` must be UUID v4 (128-bit random)
- `expires_at` = created_at + 24 hours
- `token` must be unique across all records
- Multiple unverified tokens allowed per user (latest valid)

**State Transitions**:
```
PENDING (created, not yet used)
   │
   ├─► VERIFIED (token used, user.is_verified set to true)
   │
   ├─► EXPIRED (current_time > expires_at)
   │
   └─► SUPERSEDED (new token generated, old invalidated)
```

**Business Logic**:
1. On signup: Generate token, set expires_at = now + 24h, send email
2. On verification: Check token exists, not expired, set user.is_verified = true
3. On resend: Invalidate old tokens (or mark superseded), generate new token
4. Cleanup job: Delete tokens where expires_at < now - 7 days (archive old records)

**SQLAlchemy Model**:
```python
from sqlalchemy import Integer, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
import uuid

class EmailVerification(Base):
    __tablename__ = "email_verification"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    token: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(hours=24)
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="email_verifications")
```

---

## Database Constraints Summary

### Primary Keys
- `user.id` (UUID)
- `oauth_account.id` (UUID)
- `profile.id` (INTEGER AUTOINCREMENT)
- `email_verification.id` (INTEGER AUTOINCREMENT)

### Foreign Keys
- `oauth_account.user_id` → `user.id` ON DELETE CASCADE
- `profile.user_id` → `user.id` ON DELETE CASCADE (unique)
- `email_verification.user_id` → `user.id` ON DELETE CASCADE

### Unique Constraints
- `user.email` (UNIQUE)
- `profile.user_id` (UNIQUE) — Enforces one-to-one relationship
- `oauth_account.(oauth_name, account_id)` (COMPOSITE UNIQUE)
- `email_verification.token` (UNIQUE)

### Check Constraints
- `profile.robotics_programming_experience` IN ('none', 'beginner', 'intermediate', 'advanced', 'expert')
- `profile.ai_ml_experience` IN ('none', 'beginner', 'intermediate', 'advanced', 'expert')

### Cascade Behaviors
- Delete user → Delete all oauth_accounts, profile, email_verifications (CASCADE)
- Prevents orphaned records

---

## Migrations Strategy

**Tool**: Alembic

**Migration Files**:

### 001_initial_schema.py
```python
"""Initial schema: user, oauth_account, profile, email_verification

Revision ID: 001
Revises:
Create Date: 2025-11-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

def upgrade() -> None:
    # Create user table (FastAPI-Users base)
    op.create_table(
        'user',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('email', sa.String(320), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )
    op.create_index('idx_user_email', 'user', ['email'], unique=True)

    # Create oauth_account table
    op.create_table(
        'oauth_account',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('oauth_name', sa.String(100), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=False),
        sa.Column('expires_at', sa.Integer(), nullable=True),
        sa.Column('refresh_token', sa.Text(), nullable=True),
        sa.Column('account_id', sa.String(320), nullable=False),
        sa.Column('account_email', sa.String(320), nullable=False)
    )
    op.create_index('idx_oauth_user_id', 'oauth_account', ['user_id'])
    op.create_index('idx_oauth_provider', 'oauth_account', ['oauth_name', 'account_id'], unique=True)

    # Create experience_level enum
    op.execute("CREATE TYPE experience_level AS ENUM ('none', 'beginner', 'intermediate', 'advanced', 'expert')")

    # Create profile table
    op.create_table(
        'profile',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False),
        sa.Column('robotics_programming_experience', postgresql.ENUM('none', 'beginner', 'intermediate', 'advanced', 'expert', name='experience_level'), nullable=True),
        sa.Column('ai_ml_experience', postgresql.ENUM('none', 'beginner', 'intermediate', 'advanced', 'expert', name='experience_level'), nullable=True),
        sa.Column('learning_goals', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now())
    )
    op.create_index('idx_profile_user_id', 'profile', ['user_id'], unique=True)

    # Create email_verification table
    op.create_table(
        'email_verification',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('user.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', postgresql.UUID(as_uuid=True), unique=True, nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.func.now())
    )
    op.create_index('idx_verification_token', 'email_verification', ['token'], unique=True)
    op.create_index('idx_verification_user_id', 'email_verification', ['user_id'])
    op.create_index('idx_verification_expires_at', 'email_verification', ['expires_at'])

def downgrade() -> None:
    op.drop_table('email_verification')
    op.drop_table('profile')
    op.execute('DROP TYPE experience_level')
    op.drop_table('oauth_account')
    op.drop_table('user')
```

---

## Query Patterns

### Common Queries

#### 1. Get User with Profile
```python
from sqlalchemy.orm import selectinload

async def get_user_with_profile(user_id: uuid.UUID) -> User:
    result = await session.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()
```

#### 2. Verify Email Token
```python
async def verify_email_token(token: uuid.UUID) -> EmailVerification | None:
    result = await session.execute(
        select(EmailVerification)
        .where(
            EmailVerification.token == token,
            EmailVerification.expires_at > datetime.utcnow()
        )
    )
    return result.scalar_one_or_none()
```

#### 3. Get User by Email (with OAuth Accounts)
```python
async def get_user_by_email(email: str) -> User:
    result = await session.execute(
        select(User)
        .options(selectinload(User.oauth_accounts))
        .where(User.email == email)
    )
    return result.scalar_one_or_none()
```

#### 4. Create or Update Profile
```python
async def upsert_profile(user_id: uuid.UUID, profile_data: ProfileCreate) -> Profile:
    # Check if profile exists
    result = await session.execute(
        select(Profile).where(Profile.user_id == user_id)
    )
    profile = result.scalar_one_or_none()

    if profile:
        # Update existing
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, field, value)
        profile.updated_at = datetime.utcnow()
    else:
        # Create new
        profile = Profile(user_id=user_id, **profile_data.dict())
        session.add(profile)

    await session.commit()
    await session.refresh(profile)
    return profile
```

#### 5. Cleanup Expired Tokens
```python
async def cleanup_expired_tokens():
    """Delete tokens older than 7 days (scheduled task)"""
    cutoff = datetime.utcnow() - timedelta(days=7)
    await session.execute(
        delete(EmailVerification).where(EmailVerification.expires_at < cutoff)
    )
    await session.commit()
```

---

## Performance Considerations

### Indexing Strategy
- **Email lookups**: Unique index on `user.email` (most frequent query)
- **User relationships**: Indexes on all foreign keys for JOIN performance
- **Token validation**: Unique index on `email_verification.token`
- **Cleanup queries**: Index on `email_verification.expires_at`

### Query Optimization
- Use `selectinload()` for relationships to avoid N+1 queries
- Limit SELECT to needed columns only
- Batch operations where possible (e.g., bulk user creation)

### Connection Pooling
- SQLAlchemy engine with async connection pool
- Pool size: 20 (adjust based on load testing)
- Max overflow: 10
- Neon Serverless handles connection pooling at database level

---

## Security Considerations

### Password Storage
- **Never** store plain-text passwords
- FastAPI-Users uses bcrypt by default (12 rounds)
- Hashed passwords stored in `user.hashed_password`

### Token Security
- Email verification tokens are UUID v4 (128-bit random, collision-resistant)
- Tokens expire after 24 hours
- One-time use (implied by setting `user.is_verified`)

### Data Sanitization
- Pydantic validates all inputs before database writes
- Email validation via EmailStr
- Enum constraints prevent invalid experience levels

### Cascade Deletes
- User deletion removes all related data (OAuth, profile, tokens)
- Prevents orphaned records and data leaks

---

## Testing Data Model

### Unit Tests
```python
# tests/unit/test_models.py

async def test_user_creation():
    user = User(email="test@example.com", hashed_password="hashed123")
    assert user.is_verified == False
    assert user.is_active == True

async def test_profile_relationship():
    user = User(email="test@example.com", hashed_password="hashed123")
    profile = Profile(user_id=user.id, robotics_programming_experience=ExperienceLevel.BEGINNER)
    assert profile.user == user

async def test_email_verification_expiration():
    token = EmailVerification(user_id=uuid.uuid4())
    assert token.expires_at > datetime.utcnow()
    assert token.expires_at <= datetime.utcnow() + timedelta(hours=24)
```

---

## Future Enhancements

### Potential Schema Changes
1. **User Roles Table**: Add RBAC (role-based access control)
2. **Activity Log**: Track login history, IP addresses
3. **Password History**: Prevent password reuse
4. **Two-Factor Authentication**: Add TOTP secrets table
5. **Profile Extensions**: Add avatar_url, bio, location fields

### Scalability Considerations
- Partition `email_verification` by created_at (monthly partitions)
- Archive old verification records to separate table
- Consider caching frequently accessed profiles (Redis)

---

**Data Model Complete**: All entities defined with validation rules, relationships, indexes, and migration scripts.

**Next Steps**:
1. Review data model
2. Generate API contracts (OpenAPI specs)
3. Write quickstart guide
4. Update agent context with technology stack
