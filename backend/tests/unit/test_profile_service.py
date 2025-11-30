"""
Unit tests for profile service.
Tests: T089 [US4] - test_create_profile, test_update_profile, test_upsert_logic
"""

import pytest

from src.models.profile import ExperienceLevel
from src.schemas.profile import ProfileCreate, ProfileUpdate
from src.services.profile_service import ProfileService


@pytest.mark.asyncio
async def test_create_profile(test_session, test_user):
    """Test creating a new user profile."""
    profile_data = ProfileCreate(
        robotics_experience=ExperienceLevel.BEGINNER,
        programming_experience=ExperienceLevel.INTERMEDIATE,
        ai_ml_experience=ExperienceLevel.NONE,
        learning_goals="Learn about humanoid robotics and AI",
        preferred_learning_style="hands-on",
        weekly_time_commitment=10,
    )

    profile = await ProfileService.create_profile(
        session=test_session,
        user=test_user,
        profile_data=profile_data,
    )

    assert profile is not None
    assert profile.user_id == test_user.id
    assert profile.robotics_experience == ExperienceLevel.BEGINNER
    assert profile.programming_experience == ExperienceLevel.INTERMEDIATE
    assert profile.ai_ml_experience == ExperienceLevel.NONE
    assert profile.learning_goals == "Learn about humanoid robotics and AI"
    assert profile.preferred_learning_style == "hands-on"
    assert profile.weekly_time_commitment == 10


@pytest.mark.asyncio
async def test_update_profile(test_session, test_user):
    """Test updating an existing profile."""
    # Create initial profile
    profile_data = ProfileCreate(
        robotics_experience=ExperienceLevel.BEGINNER,
        programming_experience=ExperienceLevel.BEGINNER,
        ai_ml_experience=ExperienceLevel.NONE,
        learning_goals="Initial goals",
        preferred_learning_style="visual",
        weekly_time_commitment=5,
    )

    profile = await ProfileService.create_profile(
        session=test_session,
        user=test_user,
        profile_data=profile_data,
    )

    # Update profile
    update_data = ProfileUpdate(
        robotics_experience=ExperienceLevel.INTERMEDIATE,
        learning_goals="Updated goals - build a robot",
        weekly_time_commitment=15,
    )

    updated_profile = await ProfileService.update_profile(
        session=test_session,
        profile=profile,
        profile_data=update_data,
    )

    # Check updates were applied
    assert updated_profile.robotics_experience == ExperienceLevel.INTERMEDIATE
    assert updated_profile.learning_goals == "Updated goals - build a robot"
    assert updated_profile.weekly_time_commitment == 15

    # Check unchanged fields remain the same
    assert updated_profile.programming_experience == ExperienceLevel.BEGINNER
    assert updated_profile.ai_ml_experience == ExperienceLevel.NONE
    assert updated_profile.preferred_learning_style == "visual"


@pytest.mark.asyncio
async def test_upsert_logic_create(test_session, test_user):
    """Test upsert logic when profile doesn't exist (creates new)."""
    profile_data = ProfileCreate(
        robotics_experience=ExperienceLevel.ADVANCED,
        programming_experience=ExperienceLevel.EXPERT,
        ai_ml_experience=ExperienceLevel.INTERMEDIATE,
        learning_goals="Build autonomous robots",
        preferred_learning_style="hands-on",
        weekly_time_commitment=20,
    )

    # First call should create
    profile = await ProfileService.create_or_update_profile(
        session=test_session,
        user=test_user,
        profile_data=profile_data,
    )

    assert profile is not None
    assert profile.user_id == test_user.id
    assert profile.robotics_experience == ExperienceLevel.ADVANCED


@pytest.mark.asyncio
async def test_upsert_logic_update(test_session, test_user):
    """Test upsert logic when profile already exists (updates existing)."""
    # Create initial profile
    initial_data = ProfileCreate(
        robotics_experience=ExperienceLevel.BEGINNER,
        programming_experience=ExperienceLevel.BEGINNER,
        ai_ml_experience=ExperienceLevel.NONE,
        learning_goals="Start learning",
        preferred_learning_style="visual",
        weekly_time_commitment=5,
    )

    initial_profile = await ProfileService.create_or_update_profile(
        session=test_session,
        user=test_user,
        profile_data=initial_data,
    )

    initial_id = initial_profile.id

    # Second call with updated data should update, not create new
    updated_data = ProfileCreate(
        robotics_experience=ExperienceLevel.INTERMEDIATE,
        programming_experience=ExperienceLevel.INTERMEDIATE,
        ai_ml_experience=ExperienceLevel.BEGINNER,
        learning_goals="Build practical projects",
        preferred_learning_style="hands-on",
        weekly_time_commitment=15,
    )

    updated_profile = await ProfileService.create_or_update_profile(
        session=test_session,
        user=test_user,
        profile_data=updated_data,
    )

    # Should be the same profile (same ID), just updated
    assert updated_profile.id == initial_id
    assert updated_profile.user_id == test_user.id
    assert updated_profile.robotics_experience == ExperienceLevel.INTERMEDIATE
    assert updated_profile.learning_goals == "Build practical projects"


@pytest.mark.asyncio
async def test_get_profile_by_user_id(test_session, test_user):
    """Test getting profile by user ID."""
    # No profile initially
    profile = await ProfileService.get_profile_by_user_id(
        session=test_session,
        user_id=test_user.id,
    )
    assert profile is None

    # Create profile
    profile_data = ProfileCreate(
        robotics_experience=ExperienceLevel.BEGINNER,
        programming_experience=ExperienceLevel.BEGINNER,
        ai_ml_experience=ExperienceLevel.NONE,
        learning_goals="Learn robotics",
        preferred_learning_style="visual",
        weekly_time_commitment=5,
    )

    created_profile = await ProfileService.create_profile(
        session=test_session,
        user=test_user,
        profile_data=profile_data,
    )

    # Now should find the profile
    found_profile = await ProfileService.get_profile_by_user_id(
        session=test_session,
        user_id=test_user.id,
    )

    assert found_profile is not None
    assert found_profile.id == created_profile.id
    assert found_profile.user_id == test_user.id


@pytest.mark.asyncio
async def test_delete_profile(test_session, test_user):
    """Test deleting a profile."""
    # Create profile
    profile_data = ProfileCreate(
        robotics_experience=ExperienceLevel.BEGINNER,
        programming_experience=ExperienceLevel.BEGINNER,
        ai_ml_experience=ExperienceLevel.NONE,
        learning_goals="Test deletion",
        preferred_learning_style="visual",
        weekly_time_commitment=5,
    )

    profile = await ProfileService.create_profile(
        session=test_session,
        user=test_user,
        profile_data=profile_data,
    )

    # Delete profile
    await ProfileService.delete_profile(session=test_session, profile=profile)

    # Profile should no longer exist
    deleted_profile = await ProfileService.get_profile_by_user_id(
        session=test_session,
        user_id=test_user.id,
    )

    assert deleted_profile is None
