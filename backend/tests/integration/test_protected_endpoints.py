"""
Integration tests for protected endpoints.
Tests: T067 [US3] - access /profile without auth → 401
"""

import pytest


@pytest.mark.asyncio
async def test_profile_endpoint_requires_auth(client):
    """Test that profile endpoints require authentication."""
    # Try to GET profile without authentication
    get_response = await client.get("/profile")

    assert get_response.status_code == 401

    # Try to POST profile without authentication
    profile_data = {
        "robotics_experience": "beginner",
        "programming_experience": "intermediate",
        "ai_ml_experience": "none",
        "learning_goals": "Learn robotics",
        "preferred_learning_style": "visual",
        "weekly_time_commitment": 5,
    }

    post_response = await client.post("/profile", json=profile_data)

    assert post_response.status_code == 401


@pytest.mark.asyncio
async def test_profile_endpoint_with_auth(client, verified_user):
    """Test that authenticated users can access profile endpoints."""
    # Login first
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post("/auth/login", data=login_data)
    cookies = login_response.cookies

    # Create profile
    profile_data = {
        "robotics_experience": "beginner",
        "programming_experience": "intermediate",
        "ai_ml_experience": "none",
        "learning_goals": "Learn robotics",
        "preferred_learning_style": "visual",
        "weekly_time_commitment": 5,
    }

    post_response = await client.post("/profile", json=profile_data, cookies=cookies)

    assert post_response.status_code in [200, 201]

    # Get profile
    get_response = await client.get("/profile", cookies=cookies)

    assert get_response.status_code == 200
    profile = get_response.json()
    assert profile["learning_goals"] == "Learn robotics"


@pytest.mark.asyncio
async def test_invalid_session_rejected(client):
    """Test that invalid session tokens are rejected."""
    # Use a fake cookie
    from httpx import Cookies

    fake_cookies = Cookies()
    fake_cookies.set("fastapiusersauth", "invalid-token-12345")

    response = await client.get("/auth/me", cookies=fake_cookies)

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_endpoint_requires_auth(client):
    """Test that /auth/me endpoint requires authentication."""
    response = await client.get("/auth/me")

    assert response.status_code == 401
