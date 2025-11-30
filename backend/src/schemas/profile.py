"""
Pydantic schemas for Profile model.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.profile import ExperienceLevel


class ProfileCreate(BaseModel):
    """
    Schema for creating user profiles.
    Used during onboarding process.
    """

    ai_agents_experience: ExperienceLevel
    robotics_hardware_experience: ExperienceLevel


class ProfileUpdate(BaseModel):
    """Schema for updating profile data."""

    ai_agents_experience: Optional[ExperienceLevel] = None
    robotics_hardware_experience: Optional[ExperienceLevel] = None


class ProfileRead(BaseModel):
    """
    Schema for reading profile data (responses).
    """

    id: UUID
    user_id: UUID
    ai_agents_experience: ExperienceLevel
    robotics_hardware_experience: ExperienceLevel
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
