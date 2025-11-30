"""Authentication service for token generation and verification."""

from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.email_verification import EmailVerification
from ..models.user import User


class AuthService:
    """Service for authentication-related operations."""

    @staticmethod
    async def create_verification_token(
        session: AsyncSession,
        user: User,
        expiration_hours: int = 24,
    ) -> str:
        """Create a new email verification token.

        Args:
            session: Database session
            user: User to create verification token for
            expiration_hours: Token expiration in hours (default: 24)

        Returns:
            Verification token string (UUID)
        """
        # Generate unique token
        token = str(uuid4())

        # Calculate expiration time
        expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)

        # Create verification record
        verification = EmailVerification(
            user_id=user.id,
            token=token,
            email=user.email,
            expires_at=expires_at,
        )

        session.add(verification)
        await session.commit()

        return token

    @staticmethod
    async def verify_token(session: AsyncSession, token: str) -> Optional[User]:
        """Verify an email verification token and activate user.

        Args:
            session: Database session
            token: Verification token string

        Returns:
            User object if verification successful, None otherwise
        """
        # Find verification record
        result = await session.execute(
            select(EmailVerification)
            .where(EmailVerification.token == token)
            .where(EmailVerification.is_used == False)  # noqa: E712
        )
        verification = result.scalar_one_or_none()

        if not verification or not verification.is_valid:
            return None

        # Get user
        user_result = await session.execute(
            select(User).where(User.id == verification.user_id)
        )
        user = user_result.scalar_one_or_none()

        if not user:
            return None

        # Mark user as verified
        user.is_verified = True

        # Mark token as used
        verification.is_used = True
        verification.used_at = datetime.utcnow()

        await session.commit()
        await session.refresh(user)

        return user

    @staticmethod
    async def invalidate_old_tokens(session: AsyncSession, user_id: str) -> None:
        """Invalidate all existing verification tokens for a user.

        Args:
            session: Database session
            user_id: User ID
        """
        result = await session.execute(
            select(EmailVerification)
            .where(EmailVerification.user_id == user_id)
            .where(EmailVerification.is_used == False)  # noqa: E712
        )
        tokens = result.scalars().all()

        for token in tokens:
            token.is_used = True
            token.used_at = datetime.utcnow()

        await session.commit()

    @staticmethod
    async def create_password_reset_token(
        session: AsyncSession,
        user: User,
        expiration_hours: int = 1,
    ) -> str:
        """Create a password reset token.

        Args:
            session: Database session
            user: User to create reset token for
            expiration_hours: Token expiration in hours (default: 1)

        Returns:
            Reset token string (UUID)
        """
        # For password reset, we use the same EmailVerification model
        # but could create a separate PasswordReset model if needed
        token = str(uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=expiration_hours)

        verification = EmailVerification(
            user_id=user.id,
            token=token,
            email=user.email,
            expires_at=expires_at,
        )

        session.add(verification)
        await session.commit()

        return token
