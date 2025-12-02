"""
Pydantic schemas for Profile model.
Updated for Better Auth integration.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from ..models.profile import SkillLevel, DeviceType


class ProfileCreate(BaseModel):
    """
    Schema for creating user profiles (onboarding).

    Required fields:
    - hardware_skill: Hardware/robotics experience level
    - programming_skill: Programming experience level
    - ai_ml_skill: AI/ML experience level
    - current_device: Current device/setup type
    """

    hardware_skill: SkillLevel
    programming_skill: SkillLevel
    ai_ml_skill: SkillLevel
    current_device: DeviceType


class ProfileUpdate(BaseModel):
    """Schema for updating profile data (all fields optional)."""

    hardware_skill: Optional[SkillLevel] = None
    programming_skill: Optional[SkillLevel] = None
    ai_ml_skill: Optional[SkillLevel] = None
    current_device: Optional[DeviceType] = None


class ProfileRead(BaseModel):
    """
    Schema for reading profile data (API responses).
    """

    id: UUID
    user_id: UUID
    hardware_skill: SkillLevel
    programming_skill: SkillLevel
    ai_ml_skill: SkillLevel
    current_device: DeviceType
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
