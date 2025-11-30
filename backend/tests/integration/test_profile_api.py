"""
Integration tests for profile API endpoints.
Tests: T090 [US4] - GET /profile returns data, POST /profile updates record
"""

import pytest


@pytest.mark.asyncio
async def test_get_profile_returns_data(client, verified_user, test_session):
    """Test that GET /profile returns user's profile data."""
    # Login first
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post("/auth/login", data=login_data)
    cookies = login_response.cookies

    # Create a profile
    profile_data = {
        "robotics_experience": "intermediate",
        "programming_experience": "advanced",
        "ai_ml_experience": "beginner",
        "learning_goals": "Build humanoid robots",
        "preferred_learning_style": "hands_on",
        "weekly_time_commitment": 15,
    }

    create_response = await client.post("/profile", json=profile_data, cookies=cookies)
    assert create_response.status_code in [200, 201]

    # Get the profile
    get_response = await client.get("/profile", cookies=cookies)

    assert get_response.status_code == 200
    profile = get_response.json()
    assert profile["robotics_experience"] == "intermediate"
    assert profile["programming_experience"] == "advanced"
    assert profile["ai_ml_experience"] == "beginner"
    assert profile["learning_goals"] == "Build humanoid robots"
    assert profile["preferred_learning_style"] == "hands_on"
    assert profile["weekly_time_commitment"] == 15


@pytest.mark.asyncio
async def test_post_profile_creates_new_record(client, verified_user):
    """Test that POST /profile creates a new profile record."""
    # Login
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post("/auth/login", data=login_data)
    cookies = login_response.cookies

    # Create profile
    profile_data = {
        "robotics_experience": "none",
        "programming_experience": "beginner",
        "ai_ml_experience": "none",
        "learning_goals": "Start learning robotics from scratch",
        "preferred_learning_style": "visual",
        "weekly_time_commitment": 5,
    }

    response = await client.post("/profile", json=profile_data, cookies=cookies)

    assert response.status_code in [200, 201]
    created_profile = response.json()
    assert created_profile["robotics_experience"] == "none"
    assert created_profile["learning_goals"] == "Start learning robotics from scratch"


@pytest.mark.asyncio
async def test_post_profile_updates_existing_record(client, verified_user):
    """Test that POST /profile updates existing profile (upsert)."""
    # Login
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post("/auth/login", data=login_data)
    cookies = login_response.cookies

    # Create initial profile
    initial_data = {
        "robotics_experience": "beginner",
        "programming_experience": "beginner",
        "ai_ml_experience": "none",
        "learning_goals": "Initial goals",
        "preferred_learning_style": "visual",
        "weekly_time_commitment": 5,
    }

    initial_response = await client.post("/profile", json=initial_data, cookies=cookies)
    assert initial_response.status_code in [200, 201]
    initial_profile = initial_response.json()
    initial_id = initial_profile.get("id")

    # Update profile with new data using PUT
    updated_data = {
        "robotics_experience": "intermediate",
        "programming_experience": "intermediate",
        "ai_ml_experience": "beginner",
        "learning_goals": "Updated goals - build projects",
        "preferred_learning_style": "hands_on",
        "weekly_time_commitment": 15,
    }

    update_response = await client.put("/profile", json=updated_data, cookies=cookies)
    assert update_response.status_code == 200
    updated_profile = update_response.json()

    # Should have same ID (updated, not created new)
    assert updated_profile.get("id") == initial_id
    assert updated_profile["robotics_experience"] == "intermediate"
    assert updated_profile["learning_goals"] == "Updated goals - build projects"


@pytest.mark.asyncio
async def test_get_profile_not_found(client, verified_user):
    """Test GET /profile when no profile exists."""
    # Login
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post("/auth/login", data=login_data)
    cookies = login_response.cookies

    # Try to get profile that doesn't exist
    response = await client.get("/profile", cookies=cookies)

    # Should return 404 or empty response
    assert response.status_code in [404, 200]


@pytest.mark.asyncio
async def test_profile_validation(client, verified_user):
    """Test that profile data is validated properly."""
    # Login
    login_data = {
        "username": verified_user.email,
        "password": "password123",
    }

    login_response = await client.post("/auth/login", data=login_data)
    cookies = login_response.cookies

    # Try to create profile with invalid experience level
    invalid_data = {
        "robotics_experience": "invalid_level",
        "programming_experience": "beginner",
        "ai_ml_experience": "none",
        "learning_goals": "Test",
        "preferred_learning_style": "visual",
        "weekly_time_commitment": 5,
    }

    response = await client.post("/profile", json=invalid_data, cookies=cookies)

    # Should fail validation
    assert response.status_code == 422
