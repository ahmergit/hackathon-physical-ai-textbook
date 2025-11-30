"""Clean up test user for fresh registration."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from src.database import async_session_maker


async def cleanup():
    async with async_session_maker() as session:
        # Delete verification records first (foreign key constraint)
        result = await session.execute(
            text("DELETE FROM email_verifications WHERE email = 'ahmeraziz921@gmail.com'")
        )
        print(f"Deleted {result.rowcount} verification records")
        
        # Delete user
        result = await session.execute(
            text("DELETE FROM users WHERE email = 'ahmeraziz921@gmail.com'")
        )
        print(f"Deleted {result.rowcount} users")
        
        await session.commit()
        print("Cleanup complete!")


if __name__ == "__main__":
    asyncio.run(cleanup())
