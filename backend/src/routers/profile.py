"""
Profile router for user onboarding and profile management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..dependencies.auth import current_verified_user
from ..models import Profile, User
from ..schemas import ProfileCreate, ProfileRead, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileRead)
async def get_profile(
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> ProfileRead:
    """
    Get current user's profile.

    Args:
        user: Current verified user
        session: Database session

    Returns:
        ProfileRead: User profile data

    Raises:
        HTTPException: 404 if profile not found
    """
    result = await session.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please complete onboarding.",
        )

    return profile


@router.post("", response_model=ProfileRead, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> ProfileRead:
    """
    Create user profile (onboarding).

    Args:
        profile_data: Profile creation data
        user: Current verified user
        session: Database session

    Returns:
        ProfileRead: Created profile

    Raises:
        HTTPException: 400 if profile already exists
    """
    # Check if profile already exists
    result = await session.execute(select(Profile).where(Profile.user_id == user.id))
    existing_profile = result.scalar_one_or_none()

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists. Use PUT to update.",
        )

    # Create new profile
    profile = Profile(
        user_id=user.id,
        ai_agents_experience=profile_data.ai_agents_experience,
        robotics_hardware_experience=profile_data.robotics_hardware_experience,
    )

    session.add(profile)
    await session.commit()
    await session.refresh(profile)

    return profile


@router.put("", response_model=ProfileRead)
async def update_profile(
    profile_data: ProfileUpdate,
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> ProfileRead:
    """
    Update user profile.

    Args:
        profile_data: Profile update data
        user: Current verified user
        session: Database session

    Returns:
        ProfileRead: Updated profile

    Raises:
        HTTPException: 404 if profile not found
    """
    result = await session.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found. Please create profile first.",
        )

    # Update fields
    update_data = profile_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    await session.commit()
    await session.refresh(profile)

    return profile


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    user: User = Depends(current_verified_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """
    Delete user profile.

    Args:
        user: Current verified user
        session: Database session

    Raises:
        HTTPException: 404 if profile not found
    """
    result = await session.execute(select(Profile).where(Profile.user_id == user.id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )

    await session.delete(profile)
    await session.commit()
