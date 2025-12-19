from fastapi import FastAPI
from .models import Event
from .redis_queue import enqueue
from .consumer import worker
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup():
    asyncio.create_task(worker())
    asyncio.create_task(worker())  # multi-worker

@app.post("/publish")
async def publish(events: list[Event]):
    for e in events:
        enqueue(e.dict())
    return {"status": "accepted", "count": len(events)}

@app.get("/stats")
async def stats():
    from .db import get_db
    db = await get_db()
    row = await db.fetchrow("SELECT * FROM stats")
    return dict(row)
