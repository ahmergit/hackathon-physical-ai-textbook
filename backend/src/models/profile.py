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


class ExperienceLevel(str, enum.Enum):
    """Experience level enumeration for skills assessment."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Profile(Base):
    """
    User profile model storing onboarding and learning preference data.

    Captures:
    - Robotics, programming, and AI/ML experience levels
    - Learning goals and preferences
    - Time commitment
    """

    __tablename__ = "profiles"

    # Primary key
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Foreign key to User (one-to-one)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    # Experience levels - simplified to 2 fields (stored as varchar)
    ai_agents_experience: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    robotics_hardware_experience: Mapped[str] = mapped_column(
        String(50), nullable=False
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
        return f"<Profile(user_id={self.user_id}, ai_agents={self.ai_agents_experience}, robotics_hw={self.robotics_hardware_experience})>"
