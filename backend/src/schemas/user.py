"""
Pydantic schemas for User model.
Uses FastAPI-Users schema bases.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi_users import schemas
from pydantic import EmailStr, Field


class UserRead(schemas.BaseUser[UUID]):
    """
    Schema for reading user data (responses).

    Inherits from FastAPI-Users BaseUser:
    - id: UUID
    - email: EmailStr
    - is_active: bool
    - is_superuser: bool
    - is_verified: bool
    """

    name: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class UserCreate(schemas.BaseUserCreate):
    """
    Schema for creating users (registration).

    Inherits from FastAPI-Users BaseUserCreate:
    - email: EmailStr
    - password: str (min 3 chars by default)
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255, description="User's display name")


class UserUpdate(schemas.BaseUserUpdate):
    """
    Schema for updating user data.

    Inherits from FastAPI-Users BaseUserUpdate:
    - password: Optional[str]
    - email: Optional[EmailStr]
    - is_active: Optional[bool]
    - is_superuser: Optional[bool]
    - is_verified: Optional[bool]
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255)


class UserEmailVerify(schemas.BaseModel):
    """Schema for email verification request."""

    token: str


class UserEmailVerifyResponse(schemas.BaseModel):
    """Schema for email verification response."""

    message: str
    email: EmailStr


class UserResendVerification(schemas.BaseModel):
    """Schema for resending verification email."""

    email: EmailStr
