"""
API routers for profile and chat management.
Authentication is handled by Better Auth TypeScript service.
"""

from . import profile, chat

__all__ = ["profile", "chat"]
