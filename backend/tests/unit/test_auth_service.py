"""
Unit tests for authentication service.
Tests: T048 [US1] - test_create_verification_token, test_token_expiration
"""

from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select

from src.models.email_verification import EmailVerification
from src.models.user import User
from src.services.auth_service import AuthService


@pytest.mark.asyncio
async def test_create_verification_token(test_session, test_user):
    """Test creating a verification token for a user."""
    # Create verification token
    token = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=24,
    )

    # Verify token was created
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    # Verify token exists in database
    result = await test_session.execute(
        select(EmailVerification).where(EmailVerification.token == token)
    )
    verification = result.scalar_one_or_none()

    assert verification is not None
    assert verification.user_id == test_user.id
    assert verification.email == test_user.email
    assert verification.is_used is False
    assert verification.expires_at > datetime.utcnow()


@pytest.mark.asyncio
async def test_token_expiration(test_session, test_user):
    """Test that expired tokens are properly detected."""
    # Create verification token with 1 hour expiration
    token = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=1,
    )

    # Get the verification record
    result = await test_session.execute(
        select(EmailVerification).where(EmailVerification.token == token)
    )
    verification = result.scalar_one_or_none()

    assert verification is not None
    assert verification.is_valid is True

    # Manually expire the token by setting expires_at to the past
    verification.expires_at = datetime.utcnow() - timedelta(hours=2)
    await test_session.commit()

    # Refresh to get updated data
    await test_session.refresh(verification)

    # Check that the token is now expired
    assert verification.is_valid is False

    # Try to verify with expired token - should return None
    verified_user = await AuthService.verify_token(test_session, token)
    assert verified_user is None


@pytest.mark.asyncio
async def test_verify_token_success(test_session, test_user):
    """Test successful token verification."""
    # Create verification token
    token = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=24,
    )

    # Verify token
    verified_user = await AuthService.verify_token(test_session, token)

    assert verified_user is not None
    assert verified_user.id == test_user.id
    assert verified_user.is_verified is True

    # Check that token is marked as used
    result = await test_session.execute(
        select(EmailVerification).where(EmailVerification.token == token)
    )
    verification = result.scalar_one_or_none()

    assert verification.is_used is True
    assert verification.used_at is not None


@pytest.mark.asyncio
async def test_verify_token_invalid(test_session):
    """Test verification with invalid token."""
    # Try to verify with non-existent token
    invalid_token = str(uuid4())
    verified_user = await AuthService.verify_token(test_session, invalid_token)

    assert verified_user is None


@pytest.mark.asyncio
async def test_verify_token_already_used(test_session, test_user):
    """Test that already used tokens cannot be reused."""
    # Create and verify token
    token = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=24,
    )

    # First verification should succeed
    first_verification = await AuthService.verify_token(test_session, token)
    assert first_verification is not None

    # Second verification with same token should fail
    second_verification = await AuthService.verify_token(test_session, token)
    assert second_verification is None


@pytest.mark.asyncio
async def test_invalidate_old_tokens(test_session, test_user):
    """Test invalidating all existing verification tokens for a user."""
    # Create multiple tokens
    token1 = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=24,
    )

    token2 = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=24,
    )

    # Invalidate all tokens
    await AuthService.invalidate_old_tokens(test_session, str(test_user.id))

    # Both tokens should now be marked as used
    result = await test_session.execute(
        select(EmailVerification).where(EmailVerification.user_id == test_user.id)
    )
    verifications = result.scalars().all()

    assert len(verifications) == 2
    for verification in verifications:
        assert verification.is_used is True
        assert verification.used_at is not None

    # Neither token should work for verification
    verified_user1 = await AuthService.verify_token(test_session, token1)
    verified_user2 = await AuthService.verify_token(test_session, token2)

    assert verified_user1 is None
    assert verified_user2 is None
