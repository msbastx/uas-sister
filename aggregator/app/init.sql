CREATE TABLE IF NOT EXISTS processed_events (
    topic TEXT NOT NULL,
    event_id TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    source TEXT NOT NULL,
    payload JSONB NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (topic, event_id)
);

CREATE TABLE IF NOT EXISTS stats (
    id BOOLEAN PRIMARY KEY DEFAULT TRUE,
    received BIGINT NOT NULL,
    unique_processed BIGINT NOT NULL,
    duplicate_dropped BIGINT NOT NULL
);

INSERT INTO stats (id, received, unique_processed, duplicate_dropped)
VALUES (TRUE, 0, 0, 0)
ON CONFLICT DO NOTHING;
