"""
User model for FastAPI-Users authentication.
"""

from datetime import datetime
from typing import Optional

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    User model extending FastAPI-Users base.

    Provides core authentication fields:
    - id (UUID): Primary key
    - email (str): Unique email address
    - hashed_password (str): Bcrypt hashed password
    - is_active (bool): Account active status
    - is_superuser (bool): Admin privileges
    - is_verified (bool): Email verification status

    Additional fields for our platform.
    """

    __tablename__ = "users"

    # User's display name
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Additional custom fields beyond FastAPI-Users base
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    oauth_accounts: Mapped[list["OAuthAccount"]] = relationship(
        "OAuthAccount", back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    profile: Mapped[Optional["Profile"]] = relationship(
        "Profile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    email_verifications: Mapped[list["EmailVerification"]] = relationship(
        "EmailVerification", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, verified={self.is_verified})>"
