"""
Integration tests for verification token expiration.
Tests: T100 [US5] - verify with expired token returns error
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from sqlalchemy import select

from src.models.email_verification import EmailVerification
from src.models.user import User


@pytest.mark.asyncio
async def test_expired_token_returns_error(client, test_session, test_user):
    """Test that verifying with an expired token returns an error."""
    # Create a verification token
    from src.services.auth_service import AuthService

    token = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=24,
    )

    # Manually expire the token
    result = await test_session.execute(
        select(EmailVerification).where(EmailVerification.token == token)
    )
    verification = result.scalar_one_or_none()

    assert verification is not None

    # Set expiration to the past
    verification.expires_at = datetime.utcnow() - timedelta(hours=2)
    await test_session.commit()

    # Try to verify with expired token
    verify_response = await client.post(
        "/auth/verify-email",
        json={"token": token}
    )

    # Should return error
    assert verify_response.status_code == 400
    error_data = verify_response.json()
    assert "invalid" in error_data["detail"].lower() or "expired" in error_data["detail"].lower()

    # User should still be unverified
    await test_session.refresh(test_user)
    assert test_user.is_verified is False


@pytest.mark.asyncio
async def test_valid_token_before_expiration(client, test_session, test_user):
    """Test that valid token works before expiration."""
    from src.services.auth_service import AuthService

    token = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=24,
    )

    # Verify with valid token (not expired)
    verify_response = await client.post(
        "/auth/verify-email",
        json={"token": token}
    )

    # Should succeed
    assert verify_response.status_code == 200
    verify_data = verify_response.json()
    assert verify_data["verified"] is True

    # User should be verified
    await test_session.refresh(test_user)
    assert test_user.is_verified is True


@pytest.mark.asyncio
async def test_token_expiration_boundary(client, test_session, test_user):
    """Test token expiration at the boundary (just expired vs just valid)."""
    from src.services.auth_service import AuthService

    # Create token that expires in 1 minute
    token = await AuthService.create_verification_token(
        session=test_session,
        user=test_user,
        expiration_hours=1/60,  # 1 minute
    )

    # Verify immediately (should work)
    verify_response = await client.post(
        "/auth/verify-email",
        json={"token": token}
    )

    # Should succeed as it's within the expiration window
    assert verify_response.status_code == 200
