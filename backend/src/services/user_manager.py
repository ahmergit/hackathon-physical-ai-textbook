"""
User manager for FastAPI-Users with custom verification logic.
"""

import logging
import random
import string
from typing import Optional
from uuid import UUID, uuid4

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions
from fastapi_users.models import UP
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..dependencies.user_db import get_user_db
from ..models import EmailVerification, User
from ..services.email_service import email_service

logger = logging.getLogger(__name__)


def generate_verification_code() -> str:
    """Generate a 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    """
    Custom user manager with email verification support.

    Handles:
    - User registration with email verification
    - Password reset
    - Email verification token generation
    - User lifecycle events
    - Verification check on login
    """

    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key

    async def authenticate(
        self, credentials
    ) -> Optional[UP]:
        """
        Authenticate user with credentials.
        
        Email verification is disabled - all users can login.
        """
        # Call parent authenticate
        user = await super().authenticate(credentials)
        return user

    async def validate_password(
        self, password: str, user: Optional[User] = None
    ) -> None:
        """
        Validate password strength.
        
        Requirements:
        - Minimum 8 characters
        - Must contain uppercase and lowercase
        - Must contain a digit
        
        Raises:
            InvalidPasswordException: If password doesn't meet requirements
        """
        if len(password) < 8:
            raise exceptions.InvalidPasswordException(
                reason="Password must be at least 8 characters long"
            )
        
        if not any(c.isupper() for c in password):
            raise exceptions.InvalidPasswordException(
                reason="Password must contain at least one uppercase letter"
            )
        
        if not any(c.islower() for c in password):
            raise exceptions.InvalidPasswordException(
                reason="Password must contain at least one lowercase letter"
            )
        
        if not any(c.isdigit() for c in password):
            raise exceptions.InvalidPasswordException(
                reason="Password must contain at least one digit"
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """
        Called after user registration.
        Auto-verifies user (email verification disabled).

        Args:
            user: Newly registered user
            request: Optional request context
        """
        logger.info(f"User {user.id} has registered with email {user.email}")

        # Auto-verify user since email verification is disabled
        session = self.user_db.session
        user.is_verified = True
        await session.commit()
        
        logger.info(f"User {user.email} auto-verified (email verification disabled)")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        """
        Called after password reset request.
        Sends password reset email.

        Args:
            user: User requesting password reset
            token: Password reset token
            request: Optional request context
        """
        logger.info(f"User {user.id} has requested password reset")

        # Send password reset email
        await email_service.send_password_reset_email(
            to_email=user.email, reset_token=token, user_email=user.email
        )

        logger.info(f"Password reset email sent to {user.email}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        """
        Called after verification email request.

        Args:
            user: User requesting verification
            token: Verification token
            request: Optional request context
        """
        logger.info(f"Verification requested for user {user.id}")

        # Send verification email
        await email_service.send_verification_email(
            to_email=user.email, verification_token=token, user_email=user.email
        )

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """
        Called after successful email verification.
        Sends welcome email.

        Args:
            user: Newly verified user
            request: Optional request context
        """
        logger.info(f"User {user.id} has been verified")

        # Send welcome email
        await email_service.send_welcome_email(to_email=user.email, user_name=user.email)

    async def create_verification_token(self, user: User) -> str:
        """
        Create a 6-digit email verification code in database.

        Args:
            user: User to create code for

        Returns:
            str: 6-digit verification code
        """
        # Use session from user_db instead of creating new one
        session = self.user_db.session

        # Generate 6-digit code
        code = generate_verification_code()

        # Create verification record
        verification = EmailVerification(
            user_id=user.id,
            email=user.email,
            token=code,
            expires_at=EmailVerification.create_token_expiry(hours=1),  # 1 hour for codes
            is_used=False,
        )

        session.add(verification)
        await session.commit()

        return code

    async def verify_email_token(self, token: str) -> Optional[User]:
        """
        Verify email verification token and mark user as verified.

        Args:
            token: Verification token from email

        Returns:
            User: Verified user if successful, None otherwise
        """
        # Use session from user_db instead of creating new one
        session = self.user_db.session

        # Find verification record
        result = await session.execute(
            select(EmailVerification).where(
                EmailVerification.token == token,
                EmailVerification.is_used == False,  # noqa: E712
            )
        )
        verification = result.scalar_one_or_none()

        if not verification:
            logger.warning(f"Verification token not found: {token}")
            return None

        if not verification.is_valid:
            logger.warning(f"Verification token expired or used: {token}")
            return None

        # Get user
        result = await session.execute(
            select(User).where(User.id == verification.user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.error(f"User not found for verification: {verification.user_id}")
            return None

        # Mark verification as used
        verification.is_used = True
        verification.used_at = EmailVerification.create_token_expiry(hours=0)

        # Mark user as verified
        user.is_verified = True

        await session.commit()
        await session.refresh(user)

        return user

    async def verify_email_code(self, email: str, code: str) -> Optional[User]:
        """
        Verify 6-digit email verification code and mark user as verified.

        Args:
            email: User's email address
            code: 6-digit verification code

        Returns:
            User: Verified user if successful, None otherwise
        """
        # Use session from user_db instead of creating new one
        session = self.user_db.session

        # Find verification record by email and code
        result = await session.execute(
            select(EmailVerification).where(
                EmailVerification.email == email,
                EmailVerification.token == code,
                EmailVerification.is_used == False,  # noqa: E712
            )
        )
        verification = result.scalar_one_or_none()

        if not verification:
            logger.warning(f"Verification code not found for email: {email}")
            return None

        if not verification.is_valid:
            logger.warning(f"Verification code expired for email: {email}")
            return None

        # Get user
        result = await session.execute(
            select(User).where(User.id == verification.user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            logger.error(f"User not found for verification: {verification.user_id}")
            return None

        # Mark verification as used
        verification.is_used = True
        verification.used_at = EmailVerification.create_token_expiry(hours=0)

        # Mark user as verified
        user.is_verified = True

        await session.commit()
        await session.refresh(user)

        logger.info(f"User {user.id} email verified successfully")
        return user


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> UserManager:
    """
    Dependency to get user manager instance.

    Args:
        user_db: User database adapter

    Yields:
        UserManager: User manager instance
    """
    yield UserManager(user_db)
