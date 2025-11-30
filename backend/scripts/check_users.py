"""Quick script to check users in database."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import async_session_maker
from sqlalchemy import text

async def count_users():
    async with async_session_maker() as session:
        result = await session.execute(text('SELECT COUNT(*) FROM users'))
        print(f'Total users: {result.scalar()}')
        
        result2 = await session.execute(
            text('SELECT id, email, name, is_verified, created_at FROM users ORDER BY created_at DESC')
        )
        rows = result2.fetchall()
        print('\nUsers:')
        for r in rows:
            print(f'  - {r.email} | name: {r.name} | verified: {r.is_verified}')

if __name__ == "__main__":
    asyncio.run(count_users())
