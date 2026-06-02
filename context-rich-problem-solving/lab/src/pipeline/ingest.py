from src.models.event import Event


def ingest_event(raw):
    return Event(
        user_id=raw["user_id"],
        event_type=raw["type"],
        timestamp=raw["ts"],
        value=float(raw.get("value", 0)),
    )
