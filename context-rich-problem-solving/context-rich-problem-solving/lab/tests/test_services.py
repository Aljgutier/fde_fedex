from src.pipeline.ingest import ingest_event
from src.pipeline.transform import normalize
from src.services.enrichment import enrich
from src.services.reporting import events_per_user, total_value_per_user


def _event(user_id, event_type="click", value=0.0):
    return normalize(
        ingest_event(
            {"user_id": user_id, "type": event_type, "ts": "2026-01-01T00:00:00Z", "value": value}
        )
    )


def test_enrich_adds_user_prefix_to_metadata():
    event = enrich(_event("abcdef"))
    assert event.metadata["user_prefix"] == "abc"


def test_events_per_user_counts_by_user_id():
    events = [_event("u1"), _event("u1"), _event("u2")]
    assert events_per_user(events) == {"u1": 2, "u2": 1}


def test_total_value_per_user_sums_value_field():
    events = [_event("u1", value=10), _event("u1", value=5), _event("u2", value=7)]
    assert total_value_per_user(events) == {"u1": 15.0, "u2": 7.0}
