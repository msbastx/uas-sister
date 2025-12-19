from fastapi import FastAPI
from app.redis_queue import enqueue
from app.models import Event
from app.db import get_db

app = FastAPI()


@app.post("/publish")
async def publish(events: list[Event]):
    for e in events:
        enqueue(e.dict())
    return {"status": "accepted", "count": len(events)}


@app.get("/stats")
async def stats():
    db = await get_db()
    row = await db.fetchrow(
        "SELECT received, unique_processed, duplicate_dropped FROM stats"
    )
    return dict(row)