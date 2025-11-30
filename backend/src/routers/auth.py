"""
Authentication routers for registration, login, logout, and email verification.
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..dependencies.auth import auth_backend, fastapi_users
from ..schemas import (
    ResendVerificationRequest,
    ResendVerificationResponse,
    UserCreate,
    UserRead,
    VerifyCodeRequest,
    VerifyCodeResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from ..services.user_manager import UserManager, get_user_manager
from ..utils.rate_limit import limiter

# Create router
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Include FastAPI-Users auth routers
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="",
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="",
)


@router.post("/verify-email", response_model=VerifyEmailResponse)
async def verify_email(
    data: VerifyEmailRequest,
    user_manager: UserManager = Depends(get_user_manager),
) -> VerifyEmailResponse:
    """
    Verify user email with token from verification email.

    Args:
        data: Verification request with token
        user_manager: User manager dependency

    Returns:
        VerifyEmailResponse: Verification result

    Raises:
        HTTPException: 400 if token is invalid or expired
    """
    user = await user_manager.verify_email_token(data.token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )

    return VerifyEmailResponse(
        message="Email verified successfully", email=user.email, verified=True
    )


@router.post("/verify-code", response_model=VerifyCodeResponse)
@limiter.limit("5/minute")
async def verify_code(
    request: Request,
    data: VerifyCodeRequest,
    user_manager: UserManager = Depends(get_user_manager),
) -> VerifyCodeResponse:
    """
    Verify user email with 6-digit verification code.

    Args:
        data: Verification request with email and code
        user_manager: User manager dependency

    Returns:
        VerifyCodeResponse: Verification result

    Raises:
        HTTPException: 400 if code is invalid or expired
    """
    user = await user_manager.verify_email_code(data.email, data.code)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code",
        )

    return VerifyCodeResponse(
        message="Email verified successfully", email=user.email, verified=True
    )


@router.post("/resend-verification", response_model=ResendVerificationResponse)
@limiter.limit("3/hour")
async def resend_verification(
    request: Request,
    data: ResendVerificationRequest,
    user_manager: UserManager = Depends(get_user_manager),
) -> ResendVerificationResponse:
    """
    Resend verification email to user.

    Args:
        data: Resend request with email
        user_manager: User manager dependency

    Returns:
        ResendVerificationResponse: Confirmation message

    Raises:
        HTTPException: 404 if user not found, 400 if already verified
    """
    # Get user by email
    from fastapi_users import exceptions as fu_exceptions
    
    try:
        user = await user_manager.get_by_email(data.email)
    except fu_exceptions.UserNotExists:
        # Don't reveal if user exists for security
        return ResendVerificationResponse(
            message="If the email exists, a verification link has been sent",
            email=data.email,
        )

    if not user:
        # Don't reveal if user exists for security
        return ResendVerificationResponse(
            message="If the email exists, a verification link has been sent",
            email=data.email,
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified",
        )

    # Create new verification token
    token = await user_manager.create_verification_token(user)

    # Send verification email
    from ..services.email_service import email_service

    await email_service.send_verification_email(
        to_email=user.email, verification_token=token, user_email=user.email
    )

    return ResendVerificationResponse(
        message="Verification email sent successfully", email=user.email
    )


@router.get("/me", response_model=UserRead)
async def get_current_user(
    user=Depends(fastapi_users.current_user(active=True)),
) -> UserRead:
    """
    Get current authenticated user.

    Args:
        user: Current user dependency

    Returns:
        UserRead: Current user data
    """
    return user
