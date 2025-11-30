"""
Authentication backend configuration for FastAPI-Users.
"""

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)

from ..config import settings
from ..models import User
from ..services.user_manager import get_user_manager

# Cookie transport for session management
cookie_transport = CookieTransport(
    cookie_name="physicalai_auth",
    cookie_max_age=settings.refresh_token_expire_days * 24 * 60 * 60,  # 7 days in seconds
    cookie_secure=settings.is_production,  # HTTPS only in production
    cookie_httponly=True,  # Prevent XSS attacks
    cookie_samesite="lax",  # CSRF protection
)

# Bearer transport for API access
bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    """
    Get JWT strategy for token generation.

    Returns:
        JWTStrategy: JWT strategy with configured settings
    """
    return JWTStrategy(
        secret=settings.secret_key,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
        algorithm="HS256",
    )


# Authentication backend with cookie transport
auth_backend = AuthenticationBackend(
    name="jwt-cookie",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI-Users instance
fastapi_users = FastAPIUsers[User, type(User.id)](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)

# Current user dependencies
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
