"""Authentication request/response schemas."""

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """User registration request."""

    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    """User login request (used for form validation)."""

    username: EmailStr  # FastAPI OAuth2PasswordRequestForm uses 'username'
    password: str


class VerifyRequest(BaseModel):
    """Email verification request."""

    token: str


class ResendVerificationRequest(BaseModel):
    """Resend verification email request."""

    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    """Forgot password request."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password with token."""

    token: str
    password: str


class GoogleAuthResponse(BaseModel):
    """Google OAuth authorization response."""

    authorization_url: str
