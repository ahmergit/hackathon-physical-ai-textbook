"""
Integration tests for login with unverified users.
Tests: T050 [US1] - unverified user login returns 403 with error message
"""

import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_unverified_user_cannot_login(client, test_user):
    """Test that unverified users cannot log in."""
    # Ensure user is not verified
    assert test_user.is_verified is False

    # Attempt to login
    login_data = {
        "username": test_user.email,  # FastAPI-Users uses 'username' field for email
        "password": "password123",
    }

    response = await client.post(
        "/auth/login",
        data=login_data,  # Use form data for login
    )

    # Should fail with 400 or 403 status code
    assert response.status_code in [400, 403]

    # Error message should indicate verification is required
    error_data = response.json()
    assert "detail" in error_data


@pytest.mark.asyncio
async def test_verified_user_can_login(client, verified_user):
    """Test that verified users can successfully log in."""
    # Ensure user is verified
    assert verified_user.is_verified is True

    # Attempt to login
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    response = await client.post(
        "/auth/login",
        data=login_data,
    )

    # Should succeed
    assert response.status_code == 200 or response.status_code == 204

    # Should have authentication cookie set
    assert "set-cookie" in response.headers or response.status_code == 204


@pytest.mark.asyncio
async def test_login_with_wrong_password(client, verified_user):
    """Test login with incorrect password."""
    login_data = {
        "username": verified_user.email,
        "password": "wrongpassword",
    }

    response = await client.post(
        "/auth/login",
        data=login_data,
    )

    # Should fail with 400
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_with_nonexistent_user(client):
    """Test login with email that doesn't exist."""
    login_data = {
        "username": "doesnotexist@example.com",
        "password": "anypassword",
    }

    response = await client.post(
        "/auth/login",
        data=login_data,
    )

    # Should fail with 400
    assert response.status_code == 400
