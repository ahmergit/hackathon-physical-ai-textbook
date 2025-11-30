"""Pytest configuration and fixtures for backend tests."""

import asyncio
from typing import AsyncGenerator
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base, get_async_session
from src.main import app
from src.models.user import User
from src.services.user_manager import get_user_manager


# Test database URL (SQLite in-memory for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    async_session_maker = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database session override."""

    async def override_get_async_session():
        yield test_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def sync_client(test_session: AsyncSession) -> TestClient:
    """Create synchronous test client for simple tests."""

    async def override_get_async_session():
        yield test_session

    app.dependency_overrides[get_async_session] = override_get_async_session

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(test_session: AsyncSession) -> User:
    """Create a test user."""
    from fastapi_users.password import PasswordHelper
    ph = PasswordHelper()
    
    user = User(
        id=uuid4(),
        email="test@example.com",
        hashed_password=ph.hash("password123"),
        is_active=True,
        is_verified=False,
    )

    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def verified_user(test_session: AsyncSession) -> User:
    """Create a verified test user."""
    from fastapi_users.password import PasswordHelper
    ph = PasswordHelper()
    
    user = User(
        id=uuid4(),
        email="verified@example.com",
        hashed_password=ph.hash("password123"),
        is_active=True,
        is_verified=True,
    )

    test_session.add(user)
    await test_session.commit()
    await test_session.refresh(user)

    return user


@pytest_asyncio.fixture
async def user_manager(test_session: AsyncSession):
    """Get user manager with test session."""
    from fastapi_users.db import SQLAlchemyUserDatabase
    from src.models import User
    from src.services.user_manager import UserManager

    user_db = SQLAlchemyUserDatabase(test_session, User)
    yield UserManager(user_db)
