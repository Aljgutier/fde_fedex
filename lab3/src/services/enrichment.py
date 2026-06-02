def enrich(event):
    if event.metadata is None:
        event.metadata = {}
    event.metadata["user_prefix"] = event.user_id[:3] if event.user_id else ""
    return event
