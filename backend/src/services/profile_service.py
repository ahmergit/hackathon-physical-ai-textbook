"""Profile service for managing user profiles."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.profile import Profile, ExperienceLevel
from ..models.user import User
from ..schemas.profile import ProfileCreate, ProfileUpdate


class ProfileService:
    """Service for profile-related operations."""

    @staticmethod
    async def get_profile_by_user_id(
        session: AsyncSession, user_id: UUID
    ) -> Optional[Profile]:
        """Get profile by user ID.

        Args:
            session: Database session
            user_id: User ID

        Returns:
            Profile object if found, None otherwise
        """
        result = await session.execute(
            select(Profile).where(Profile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_profile(
        session: AsyncSession, user: User, profile_data: ProfileCreate
    ) -> Profile:
        """Create a new profile for a user.

        Args:
            session: Database session
            user: User to create profile for
            profile_data: Profile creation data

        Returns:
            Created Profile object
        """
        profile = Profile(
            user_id=user.id,
            robotics_experience=profile_data.robotics_experience,
            programming_experience=profile_data.programming_experience,
            ai_ml_experience=profile_data.ai_ml_experience,
            learning_goals=profile_data.learning_goals,
            preferred_learning_style=profile_data.preferred_learning_style,
            weekly_time_commitment=profile_data.weekly_time_commitment,
        )

        session.add(profile)
        await session.commit()
        await session.refresh(profile)

        return profile

    @staticmethod
    async def update_profile(
        session: AsyncSession, profile: Profile, profile_data: ProfileUpdate
    ) -> Profile:
        """Update an existing profile.

        Args:
            session: Database session
            profile: Existing profile to update
            profile_data: Profile update data

        Returns:
            Updated Profile object
        """
        # Update only fields that are provided
        update_data = profile_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(profile, field, value)

        await session.commit()
        await session.refresh(profile)

        return profile

    @staticmethod
    async def create_or_update_profile(
        session: AsyncSession, user: User, profile_data: ProfileCreate
    ) -> Profile:
        """Create or update profile (upsert logic).

        Args:
            session: Database session
            user: User to create/update profile for
            profile_data: Profile data

        Returns:
            Created or updated Profile object
        """
        existing_profile = await ProfileService.get_profile_by_user_id(
            session, user.id
        )

        if existing_profile:
            # Update existing profile
            profile_update = ProfileUpdate(**profile_data.model_dump())
            return await ProfileService.update_profile(
                session, existing_profile, profile_update
            )
        else:
            # Create new profile
            return await ProfileService.create_profile(session, user, profile_data)

    @staticmethod
    async def delete_profile(session: AsyncSession, profile: Profile) -> None:
        """Delete a profile.

        Args:
            session: Database session
            profile: Profile to delete
        """
        await session.delete(profile)
        await session.commit()
