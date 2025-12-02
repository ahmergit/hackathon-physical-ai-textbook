"""
User profile model for onboarding data.
"""

import enum
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class SkillLevel(str, enum.Enum):
    """Skill level enumeration for hardware, programming, and AI/ML."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


class DeviceType(str, enum.Enum):
    """Current device/setup type enumeration."""

    CLOUD_LAPTOP = "cloud_laptop"
    RTX_GPU = "rtx_gpu"
    PHYSICAL_ROBOT = "physical_robot"


class Profile(Base):
    """
    User profile model storing onboarding and learning preference data.

    Captures (Better Auth integration):
    - Hardware/robotics skill level (beginner, intermediate, expert)
    - Programming skill level (beginner, intermediate, expert)
    - AI/ML skill level (beginner, intermediate, expert)
    - Current device/setup (cloud_laptop, rtx_gpu, physical_robot)
    """

    __tablename__ = "profiles"

    # Primary key
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Foreign key to User (one-to-one)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    # New skill level fields (Better Auth schema)
    # Use values_callable to tell SQLAlchemy to use lowercase enum values for PostgreSQL
    hardware_skill: Mapped[SkillLevel] = mapped_column(
        Enum(SkillLevel, name='skilllevel', create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    programming_skill: Mapped[SkillLevel] = mapped_column(
        Enum(SkillLevel, name='skilllevel', create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    ai_ml_skill: Mapped[SkillLevel] = mapped_column(
        Enum(SkillLevel, name='skilllevel', create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    current_device: Mapped[DeviceType] = mapped_column(
        Enum(DeviceType, name='devicetype', create_type=False, values_callable=lambda x: [e.value for e in x]), nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="profile")

    def __repr__(self) -> str:
        return f"<Profile(user_id={self.user_id}, hw={self.hardware_skill}, prog={self.programming_skill}, ai={self.ai_ml_skill}, device={self.current_device})>"
