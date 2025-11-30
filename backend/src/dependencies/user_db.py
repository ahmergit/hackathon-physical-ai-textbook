"""
User database adapter for FastAPI-Users.
"""

from typing import AsyncGenerator
from uuid import UUID

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..models import User


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """
    Dependency to provide FastAPI-Users database adapter.

    Args:
        session: Database session

    Yields:
        SQLAlchemyUserDatabase: User database adapter
    """
    yield SQLAlchemyUserDatabase(session, User)
