"""
Integration tests for session persistence.
Tests: T066 [US3] - login → GET /me (valid) → logout → GET /me (401)
"""

import pytest
from httpx import Cookies


@pytest.mark.asyncio
async def test_session_persistence_flow(client, verified_user):
    """Test complete session lifecycle: login, access protected resource, logout."""

    # Step 1: Login
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post(
        "/auth/login",
        data=login_data,
    )

    assert login_response.status_code in [200, 204]

    # Extract cookies from login response
    cookies = login_response.cookies

    # Step 2: Access protected endpoint (/me) with session
    me_response = await client.get(
        "/auth/me",
        cookies=cookies,
    )

    assert me_response.status_code == 200
    user_data = me_response.json()
    assert user_data["email"] == verified_user.email
    assert user_data["is_verified"] is True

    # Step 3: Logout
    logout_response = await client.post(
        "/auth/logout",
        cookies=cookies,
    )

    assert logout_response.status_code in [200, 204]

    # Step 4: Try to access protected endpoint after logout (should fail)
    me_after_logout_response = await client.get("/auth/me")

    assert me_after_logout_response.status_code == 401


@pytest.mark.asyncio
async def test_session_cookie_set_on_login(client, verified_user):
    """Test that session cookie is properly set on login."""
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    response = await client.post(
        "/auth/login",
        data=login_data,
    )

    assert response.status_code in [200, 204]

    # Check that cookies were set
    assert len(response.cookies) > 0


@pytest.mark.asyncio
async def test_access_protected_endpoint_without_auth(client):
    """Test accessing protected endpoint without authentication."""
    response = await client.get("/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_session_persists_across_requests(client, verified_user):
    """Test that session persists across multiple requests."""
    # Login
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post(
        "/auth/login",
        data=login_data,
    )

    cookies = login_response.cookies

    # Make multiple requests with same session
    for _ in range(3):
        response = await client.get("/auth/me", cookies=cookies)
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == verified_user.email
