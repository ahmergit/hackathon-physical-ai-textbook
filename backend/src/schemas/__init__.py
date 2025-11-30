"""
Pydantic schemas for API request/response models.
"""

from .email_verification import (
    EmailVerificationCreate,
    EmailVerificationRead,
    ResendVerificationRequest,
    ResendVerificationResponse,
    VerifyCodeRequest,
    VerifyCodeResponse,
    VerifyEmailRequest,
    VerifyEmailResponse,
)
from .profile import ProfileCreate, ProfileRead, ProfileUpdate
from .user import (
    UserCreate,
    UserEmailVerify,
    UserEmailVerifyResponse,
    UserRead,
    UserResendVerification,
    UserUpdate,
)

__all__ = [
    # User schemas
    "UserRead",
    "UserCreate",
    "UserUpdate",
    "UserEmailVerify",
    "UserEmailVerifyResponse",
    "UserResendVerification",
    # Profile schemas
    "ProfileRead",
    "ProfileCreate",
    "ProfileUpdate",
    # Email verification schemas
    "EmailVerificationRead",
    "EmailVerificationCreate",
    "VerifyEmailRequest",
    "VerifyEmailResponse",
    "VerifyCodeRequest",
    "VerifyCodeResponse",
    "ResendVerificationRequest",
    "ResendVerificationResponse",
]
