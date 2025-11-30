"""
Integration tests for user registration flow.
Tests: T049 [US1] - POST /register → verify email sent → POST /verify → user.is_verified=true
"""

import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy import select

from src.models.user import User
from src.models.email_verification import EmailVerification


@pytest.mark.asyncio
async def test_registration_flow_complete(client, test_session):
    """Test complete registration flow from signup to verification."""

    # Mock email service to prevent actual email sending
    with patch("src.services.email_service.email_service.send_verification_email", new_callable=AsyncMock) as mock_email:
        # Step 1: Register new user
        registration_data = {
            "email": "newuser@example.com",
            "password": "SecurePass123!",
        }

        register_response = await client.post("/auth/register", json=registration_data)

        assert register_response.status_code in [200, 201]
        user_data = register_response.json()
        assert user_data["email"] == "newuser@example.com"
        assert user_data["is_verified"] is False

        # Verify email was sent
        assert mock_email.called

        # Step 2: Get verification token from database
        result = await test_session.execute(
            select(EmailVerification)
            .join(User)
            .where(User.email == "newuser@example.com")
            .where(EmailVerification.is_used == False)
        )
        verification = result.scalar_one_or_none()

        assert verification is not None
        assert verification.is_valid is True
        token = verification.token

        # Step 3: Verify email with token
        verify_response = await client.post(
            "/auth/verify-email",
            json={"token": token}
        )

        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        assert verify_data["verified"] is True
        assert verify_data["email"] == "newuser@example.com"

        # Step 4: Verify user is now marked as verified in database
        user_result = await test_session.execute(
            select(User).where(User.email == "newuser@example.com")
        )
        user = user_result.scalar_one_or_none()

        assert user is not None
        assert user.is_verified is True


@pytest.mark.asyncio
async def test_registration_with_invalid_email(client):
    """Test registration with invalid email format."""
    registration_data = {
        "email": "not-an-email",
        "password": "SecurePass123!",
    }

    response = await client.post("/auth/register", json=registration_data)

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_registration_with_weak_password(client):
    """Test registration with password that doesn't meet requirements."""
    registration_data = {
        "email": "user@example.com",
        "password": "weak",  # Too short, no complexity
    }

    response = await client.post("/auth/register", json=registration_data)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_verification_with_invalid_token(client):
    """Test email verification with invalid token."""
    verify_response = await client.post(
        "/auth/verify-email",
        json={"token": "invalid-token-12345"}
    )

    assert verify_response.status_code == 400
    error_data = verify_response.json()
    assert "invalid" in error_data["detail"].lower() or "expired" in error_data["detail"].lower()


@pytest.mark.asyncio
async def test_duplicate_email_registration(client, test_user):
    """Test that registering with an existing email is rejected."""
    registration_data = {
        "email": test_user.email,
        "password": "NewPassword123!",
    }

    with patch("src.services.email_service.email_service.send_verification_email", new_callable=AsyncMock):
        response = await client.post("/auth/register", json=registration_data)

    assert response.status_code == 400
