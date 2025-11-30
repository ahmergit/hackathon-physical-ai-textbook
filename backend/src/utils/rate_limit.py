"""Rate limiting utilities for API endpoints."""

from slowapi import Limiter
from slowapi.util import get_remote_address


# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/hour"],
    storage_uri="memory://",
)


def get_limiter() -> Limiter:
    """Get the rate limiter instance.

    Returns:
        Limiter: The configured rate limiter
    """
    return limiter
