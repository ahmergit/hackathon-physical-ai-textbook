"""
OAuth account model for social authentication.
"""

from datetime import datetime
from uuid import UUID

from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    """
    OAuth account model for external authentication providers (Google).

    Extends FastAPI-Users OAuth base with:
    - oauth_name (str): Provider name (e.g., "google")
    - account_id (str): Provider's user ID
    - account_email (str): Email from provider
    - access_token (str): OAuth access token
    - refresh_token (str): OAuth refresh token
    - expires_at (int): Token expiration timestamp
    """

    __tablename__ = "oauth_accounts"

    # Foreign key to User
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Additional timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="oauth_accounts")

    def __repr__(self) -> str:
        return f"<OAuthAccount(oauth_name={self.oauth_name}, account_email={self.account_email})>"
