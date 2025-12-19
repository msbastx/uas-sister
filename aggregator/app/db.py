import asyncpg
import os
import asyncio

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db(retries=10):
    for i in range(retries):
        try:
            return await asyncpg.connect(DATABASE_URL)
        except Exception as e:
            print(f"[DB] retry {i+1}/{retries}...")
            await asyncio.sleep(2)
    raise RuntimeError("Database not available")
