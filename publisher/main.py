import requests
import uuid

import time
time.sleep(8)

import random

URL = "http://aggregator:8080/publish"

while True:
    events = []
    for _ in range(10):
        eid = str(uuid.uuid4()) if random.random() > 0.3 else "DUPLICATE"
        events.append({
            "topic": "test",
            "event_id": eid,
            "timestamp": "2025-01-01T00:00:00Z",
            "source": "publisher",
            "payload": {"value": random.randint(1,100)}
        })

    requests.post(URL, json=events)
