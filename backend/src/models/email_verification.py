"""
Email verification model for tracking verification tokens.
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class EmailVerification(Base):
    """
    Email verification token model.

    Stores verification tokens with 24-hour expiration.
    One-time use tokens are marked as used after verification.
    """

    __tablename__ = "email_verifications"

    # Primary key
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Foreign key to User
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Verification token (UUID)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    # Email being verified
    email: Mapped[str] = mapped_column(String(255), nullable=False)

    # Expiration (default 24 hours)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Usage tracking
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="email_verifications")

    def __repr__(self) -> str:
        return f"<EmailVerification(email={self.email}, expires_at={self.expires_at}, used={self.is_used})>"

    @property
    def is_expired(self) -> bool:
        """Check if token has expired."""
        return datetime.utcnow() > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if token is valid (not used and not expired)."""
        return not self.is_used and not self.is_expired

    @staticmethod
    def create_token_expiry(hours: int = 24) -> datetime:
        """
        Create expiration timestamp for verification token.

        Args:
            hours: Number of hours until expiration (default: 24)

        Returns:
            datetime: Expiration timestamp
        """
        return datetime.utcnow() + timedelta(hours=hours)
