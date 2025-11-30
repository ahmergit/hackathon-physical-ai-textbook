"""
Pydantic schemas for Email Verification.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class EmailVerificationCreate(BaseModel):
    """Schema for creating email verification tokens (internal use)."""

    email: EmailStr
    hours_valid: int = 24


class EmailVerificationRead(BaseModel):
    """Schema for reading email verification data."""

    id: UUID
    user_id: UUID
    email: EmailStr
    token: str
    expires_at: datetime
    is_used: bool
    created_at: datetime

    class Config:
        from_attributes = True


class VerifyEmailRequest(BaseModel):
    """Schema for email verification request from user."""

    token: str


class VerifyEmailResponse(BaseModel):
    """Schema for email verification response."""

    message: str
    email: EmailStr
    verified: bool


class VerifyCodeRequest(BaseModel):
    """Schema for verifying 6-digit email verification code."""

    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")


class VerifyCodeResponse(BaseModel):
    """Schema for verify code response."""

    message: str
    email: EmailStr
    verified: bool


class ResendVerificationRequest(BaseModel):
    """Schema for resending verification email."""

    email: EmailStr


class ResendVerificationResponse(BaseModel):
    """Schema for resend verification response."""

    message: str
    email: EmailStr
