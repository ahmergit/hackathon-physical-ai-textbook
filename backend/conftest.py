"""
Pytest configuration and shared fixtures.
Provides test database, client, and authentication utilities.
"""

import asyncio
from typing import AsyncGenerator, Generator
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.database import Base, get_async_session
from src.main import app
from src.models.user import User
from src.models.profile import Profile
from src.models.email_verification import EmailVerification
from src.dependencies.auth import get_user_manager
from src.config import settings


# Test database URL (use in-memory SQLite for fast tests)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test HTTP client with database session override."""

    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user = User(
        email="test@example.com",
        hashed_password=pwd_context.hash("Test123!"),
        is_active=True,
        is_verified=True,
        is_superuser=False,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def unverified_user(db_session: AsyncSession) -> User:
    """Create an unverified test user."""
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    user = User(
        email="unverified@example.com",
        hashed_password=pwd_context.hash("Test123!"),
        is_active=True,
        is_verified=False,
        is_superuser=False,
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def test_profile(db_session: AsyncSession, test_user: User) -> Profile:
    """Create a test profile."""
    from src.schemas.profile import ExperienceLevel

    profile = Profile(
        user_id=test_user.id,
        robotics_programming_experience=ExperienceLevel.INTERMEDIATE,
        ai_ml_experience=ExperienceLevel.BEGINNER,
        learning_goals="Learn robot control systems",
    )

    db_session.add(profile)
    await db_session.commit()
    await db_session.refresh(profile)

    return profile


@pytest_asyncio.fixture
async def verification_token(db_session: AsyncSession, unverified_user: User) -> str:
    """Create a verification token for an unverified user."""
    token = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(hours=24)

    verification = EmailVerification(
        user_id=unverified_user.id,
        token=token,
        email=unverified_user.email,
        expires_at=expires_at,
    )

    db_session.add(verification)
    await db_session.commit()

    return token


@pytest_asyncio.fixture
async def expired_verification_token(db_session: AsyncSession, unverified_user: User) -> str:
    """Create an expired verification token."""
    token = str(uuid4())
    expires_at = datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago

    verification = EmailVerification(
        user_id=unverified_user.id,
        token=token,
        email=unverified_user.email,
        expires_at=expires_at,
    )

    db_session.add(verification)
    await db_session.commit()

    return token


@pytest_asyncio.fixture
async def authenticated_client(
    client: AsyncClient,
    test_user: User,
) -> AsyncClient:
    """Create an authenticated test client."""
    # Log in the test user
    response = await client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "Test123!",
        },
    )

    assert response.status_code == 200

    return client


@pytest.fixture
def mock_sendgrid(monkeypatch):
    """Mock SendGrid email service."""
    sent_emails = []

    async def mock_send_verification_email(email: str, token: str):
        sent_emails.append({"email": email, "token": token})
        return True

    monkeypatch.setattr(
        "src.services.email_service.send_verification_email",
        mock_send_verification_email,
    )

    return sent_emails
