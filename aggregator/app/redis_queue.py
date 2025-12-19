import redis
import os
import json

r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

QUEUE = "events"

def enqueue(event: dict):
    r.rpush(QUEUE, json.dumps(event))

def dequeue():
    data = r.blpop(QUEUE, timeout=1)
    return json.loads(data[1]) if data else None
