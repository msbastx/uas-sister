import asyncio
from .redis_queue import dequeue
from .db import get_db

async def worker():
    db = await get_db()

    while True:
        event = dequeue()
        if not event:
            await asyncio.sleep(0.1)
            continue

        async with db.transaction():
            # INSERT idempotent
            status = await db.execute("""
                INSERT INTO processed_events
                (topic, event_id, timestamp, source, payload)
                VALUES ($1,$2,$3,$4,$5)
                ON CONFLICT DO NOTHING
            """,
            event["topic"],
            event["event_id"],
            event["timestamp"],
            event["source"],
            event["payload"])

            # asyncpg returns: "INSERT 0 1" or "INSERT 0 0"
            inserted = status.split()[-1] == "1"

            if inserted:
                await db.execute("""
                    UPDATE stats
                    SET unique_processed = unique_processed + 1
                    WHERE id = 1
                """)
            else:
                await db.execute("""
                    UPDATE stats
                    SET duplicate_dropped = duplicate_dropped + 1
                    WHERE id = 1
                """)